from flask import Flask, request, jsonify
import requests
from datetime import datetime as dt
import logging


app = Flask(__name__)
attending_database = []
patient_database = []


@app.route("/", methods=["GET"])
def status():
    """States that server is on feedback message

    Returns:
        string: "Server is on"
    """
    return "Server is on"


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """Accepts json request and posts new patient
    to server database.

    Method curated by Anuj Som

    json request should contain a dict formatted as follows:
    {
        "patient_id": int/str,      # id # or # in string
        "attending_username": str,  # Physician name formatted as:
                                      "Lastname.Firstinitial"
        "patient_age": int/str,     # age # of years or # of years in string
    }
    Method will validate input and post valid patient information
    to server

    Returns:
        dict: patient dictionary added to database
    """
    # Accept and validate input
    in_data = request.get_json()
    expected_values = {"patient_id": [int, str],
                       "attending_username": [str],
                       "patient_age": [int, str]}
    error_string, status_code = validate_dict_input(in_data, expected_values)
    if error_string is not True:
        return error_string, status_code

    # It is noted that attending_username will already exist
    # within attending database

    # External method handlers
    new_patient = add_patient_to_database(in_data["patient_id"],
                                          in_data["attending_username"],
                                          in_data["patient_age"])

    # Data output & return
    return "Added patient {}".format(new_patient), 200


@app.route("/api/new_attending", methods=["POST"])
def new_attending():
    """Accepts json request and posts new attending
    information to server database.

    Method curated by Braden Garrison

    json request should contain a dict formatted as follows:
    {
        "attending_username": str,  # Physician name formatted as:
                                      "Lastname.Firstinitial"
        "attending_email": str,     # email, "dr_user_id@yourdomain.com"
        "attending_phone": str      # Phone #, "###-###-####"
    }
    This method will be used to create a new attending physician,
    as specified by the add_attending_to_databasee() method

    Returns:
        dict: attending dict added to database
    """
    # Accept and validate attending input
    in_data = request.get_json()
    expected_values = {"attending_username": [str],
                       "attending_email": [str],
                       "attending_phone": [str]}
    error_string, status_code = validate_dict_input(in_data, expected_values)
    if error_string is not True:
        return error_string, status_code

    # External methods
    attending = add_attending_to_database(in_data["attending_username"],
                                          in_data["attending_email"],
                                          in_data["attending_phone"])

    # Data output and return
    return "Added attending {}".format(attending), 200


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """Accepts json request and posts new patient heart rate
    to server database.

    Method curated by Braden Garrison

    json request should contain a dict formatted as follows:
    {
        "patient_id": int, # Should be patient MRN
        "heart_rate": int
    }
    This method will be used to match heart-rate
    information to an existing patient,
    as specified by the patient_id

    Returns:
        int: Fetched heart rate
    """
    # Accept and validate id and heart rate input
    in_data = request.get_json()
    expected_values = {"patient_id": [str, int],
                       "heart_rate": [str, int]}
    error_string, status_code = validate_dict_input(in_data, expected_values)
    if error_string is not True:
        return error_string, status_code

    # Match patient and update heart rate information
    patient = get_patient_from_database(str_to_int(in_data["patient_id"])[0])
    if (type(patient)) == str:
        return patient, 400
    add_hr = add_heart_rate(patient, str_to_int(in_data["heart_rate"])[0])

    # Data output and return
    return "Added heart rate information {} "
    "for patient id {}".format(add_hr, in_data["patient_id"]), 200


@app.route("/api/status/<patient_id>", methods=["GET"])
def status_pid(patient_id):
    """Accepts patient id and returns json containing
    latest heart rate, status, and timestamp.

    Method curated by Anuj Som

    <patient_id> request should contain an existing pid.
    The output will return a json dict formatted as follows:
    {
        "heart_rate": int,
        "status":  str ("tachycardic" | "not tachycardic"),
        "timestamp": str ("2018-03-09 11:00:36")
    }
    This method will be used to tell if specified patient
    is tachycardic or not, and the time of the most recent
    heart rate. If no recent heart rate reported, returns
    None

    Returns:
        string: Status
        None: No HR data exists
    """
    # Accept and validate input
    in_data = patient_id
    check = str_to_int(in_data)
    if(not check[1]):
        return "Invalid patient ID", 400
    pid = check[0]

    patient = get_patient_from_database(pid)
    if(type(patient) == str):
        return patient, 400

    # External method handlers
    patData = get_last_heart_rate(patient)

    # Data output & return
    return jsonify(patData), 200


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate_pid(patient_id):
    """Variable URL route that accepts a patient id and
    returns a list of all previous heart rate measurements
    for that patient.

    Method curated by Braden Garrison

    <patient_id> request should contain an existing pid.
    If no patient is found with a pid matching <patient_id>,
    an error string indicating no patient found will be returned.
    This method will be used to view all the previously input
    heart rates for a specified patient.

    Returns:
        list: list of integers of saved heart rate values
        string: error message string will be returned if no
        matching patient id is found in the database
    """
    in_data = patient_id
    check = str_to_int(in_data)
    if(not check[1]):
        return "Invalid patient ID", 400
    pid = check[0]

    patient = get_patient_from_database(pid)
    if (type(patient)) == str:
        return patient, 400

    hr_list = prev_heart_rate(patient)
    return hr_list, 200


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_avg_pid(patient_id):
    """Variable URL route that accepts a patient id and
    returns patient's average heart rate across all measurements.

    Method curated by Braden Garrison

    <patient_id> request should contain an existing pid.
    If no patient is found with a pid matching <patient_id>,
    an error string indicating no patient found will be returned.
    This method will be used to view the integer average of all
    stored heart values for a patient.

    Returns:
        int: average patient heart rate of all measurements as an integer
        string: error message string will be returned if no
        matching patient id is found in the database
    """
    in_data = patient_id
    check = str_to_int(in_data)
    if(not check[1]):
        return "Invalid patient ID", 400
    pid = check[0]

    patient = get_patient_from_database(pid)
    if (type(patient)) == str:
        return patient, 400

    hr_list = prev_heart_rate(patient)
    hr_avg = heart_rate_average(hr_list)
    return hr_avg, 200


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def heart_rate_interval_avg():
    """Accepts json request and posts new patient heart rate
    to server database.

    Method curated by Braden Garrison

    json request should contain a dict formatted as follows:
    {
        "patient_id": int, # Should be patient MRN
        "heart_rate_average_since": str # Should be formatted in form:
                                        # "2018-03-09 11:00:36"
    }
    This method will be used to calculate and return the heart
    rate interval average of a specified patient since the given
    date/time.

    Returns:
        int: heart rate interval average
    """
    in_data = request.get_json()
    expected_values = {"patient_id": [str, int],
                       "heart_rate_average_since": [str]}
    error_string, status_code = validate_dict_input(in_data, expected_values)
    if error_string is not True:
        return error_string, status_code

    patient = get_patient_from_database(str_to_int(in_data["patient_id"])[0])
    if (type(patient)) == str:
        return patient, 400
    hr_interval = heart_rate_interval(in_data["heart_rate_average_since"],
                                      patient)
    hr_int_avg = heart_rate_average(hr_interval)
    return hr_int_avg, 200


@app.route("/api/patients/<attending_username>", methods=["GET"])
def patients_attending_username(attending_username):
    """Accepts attending name and returns a list of patients
    that attending is responsible for by querying the database.

    Method curated by Anuj Som

    <attending_username> request should contain a name formatted as
    "Lastname.Firstinitial".
    The output will return a json string formatted as follows:
    {
        "patient_id": int,                           # pid
        "last_heart_rate": int,                      # heart rate
        "last_time": (str) "2018-03-09 11:00:36",    # datetime string
        "status":  "tachycardic" | "not tachycardic" # status
    }
    This method will return an error if attending not found.
    Additionally, will return an empty list if no patients associated
    with provided attending.

    Returns:
        string: json string formatted as above
    """
    # Accept and validate input
    in_data = attending_username
    attending = get_attending_from_database(in_data)
    if(type(attending) == str):
        return attending, 400

    # External method handlers

    # Assumes all patients within attending list are existing
    # patients (since patients only added to an attending's list)
    # with new_patient call
    patList = []
    pats = attending["patients"]
    for pat in pats:
        pat_info = get_last_heart_rate(pat)
        if(pat_info is None):
            newDict = {
                "patient_id": pat["id"],
                "last_heart_rate": pat_info["heart_rate"],
                "last_time": pat_info["timestamp"],
                "status": pat_info["status"]
            }
            patList.append(newDict)

    # Data output & return
    return jsonify(patList), 200


def validate_dict_input(in_data, expected_keys):
    """Validate the presence of expected keys, value types of
    in_data

    Format expected_keys as follows:

    expected_keys = {
        "key1": [allowed_type1, allowed_type2,...],
        "key2": [allowed_type1, allowed_type2,...],
        ...
    }

    This method will return true only if all expected keys
    exist within in in_data and all in_data value types
    are allowed

    Note that user may need to include functionality
    for allowed types to verify certain cases

    Args:
        in_data (dict(string:obj)): dictionary input data
        expected_keys (dict(string:list)):

    Returns:
        [type]: [description]
    """
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    for key in expected_keys:
        # Ensure all expected keys exist within in_data
        if key not in in_data:
            return "The key {} is missing from input".format(key), 400

        # Ensure all types are valid
        if type(in_data[key]) not in expected_keys[key]:
            return "The key {} has invalid data type".format(key), 400

        # Verify str are able to cleanly cast to int
        if set(expected_keys[key]) == set([str, int]):
            check = str_to_int(in_data[key])
            if not check[1]:
                m1 = "The value \"{}\"".format(in_data[key])
                m2 = " in key {} cannot be cast to int".format(key)
                return m1+m2, 400

    return True, 200


def add_patient_to_database(pat_id, att_name, pat_age):
    patient = {
            "id": str_to_int(pat_id)[0],
            "age": str_to_int(pat_age)[0],
            "attending": att_name,
            "HR_data": []
        }
    patient_database.append(patient)
    attendant = get_attending_from_database(att_name)
    attendant["patients"].append(patient)
    logging.info('Registered new patient with ID {}'.format(pat_id))
    return patient


def get_patient_from_database(id_no):
    patlist = [x for x in patient_database if x["id"] == id_no]
    if len(patlist) == 0:
        return "ERROR: no patient with id {} in database".format(id_no)
    if len(patlist) > 1:
        return "ERROR: patient id not unique identifier"
    return patlist[0]


def add_attending_to_database(att_name, att_email, att_phone):
    attendant = {
            "name": att_name,
            "email": att_email,
            "phone": att_phone,
            "patients": []
        }
    attending_database.append(attendant)
    logging.info('Registered new attending physician with username {} '
                 'and email {}'.format(att_name, att_email))
    return attendant


def get_attending_from_database(attendant_name):
    attlist = [x for x in attending_database if x["name"] == attendant_name]
    if len(attlist) == 0:
        return "ERROR: no attending in database"
    if len(attlist) > 1:
        return "ERROR: name not unique identifier"
    return attlist[0]


def add_heart_rate(patient, heart_rate):
    timestamp = dt.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    tach = is_tachycardic(heart_rate, patient["age"])
    if tach == "tachycardic":
        att, email = tach_warning(patient, heart_rate)
        tach_email(patient, att, email)
    hr_info = {"heart_rate": heart_rate,
               "status": tach,
               "timestamp": timestamp}
    patient["HR_data"].append(hr_info)
    return hr_info


def get_last_heart_rate(patient):
    HR_data = patient["HR_data"]
    if len(HR_data) == 0:
        return None
    return HR_data[-1]


def is_tachycardic(hr, age):
    """Evaluates if posted heart rate is tachycardic

    Tachycardia is defined as a heart rate that is above normal resting
    rate. Specific tachycardic values are dependent upon patient age. More
    info about tachycardia and its diagnosis can be found at:
    https://en.wikipedia.org/wiki/Tachycardia

    Args:
        hr (int): accepts posted heart rate as an int
        age (int): accepts patient age as an int

    Returns:
        str: string describing result - "tachycardic" or "not tachycardic"
    """
    if 1 <= age < 3:
        if hr > 151:
            tach = "tachycardic"
        else:
            tach = "not tachycardic"
    elif 3 <= age < 5:
        if hr > 137:
            tach = "tachycardic"
        else:
            tach = "not tachycardic"
    elif 5 <= age < 8:
        if hr > 133:
            tach = "tachycardic"
        else:
            tach = "not tachycardic"
    elif 8 <= age < 12:
        if hr > 130:
            tach = "tachycardic"
        else:
            tach = "not tachycardic"
    elif 12 <= age < 15:
        if hr > 119:
            tach = "tachycardic"
        else:
            tach = "not tachycardic"
    else:
        if hr > 100:
            tach = "tachycardic"
        else:
            tach = "not tachycardic"
    return tach


def tach_warning(patient, hr):
    """Creates log entry upon server receiving tachycardic HR post

    Tachycardic heart rate values are defined in the is_tachycardic
    function. Any heart rate values exceeding the specified range for
    the patient age will create a warning-level log entry.

    Args:
        patient (dict): Accepts patient dict containing all patient info
        hr (int): Accepts posted heart rate as integer

    Returns:
        dict: returns attending dictionary containing all attending info
        str: returns attending email
    """
    att = get_attending_from_database(patient["attending"])
    email = att["email"]
    logging.warning('Tachycardic heart rate of {} posted for patient ID {}. '
                    'Contacting attending via email: {}'.format(
                     hr, patient["id"], email))
    return att, email


def tach_email(patient, att, email):
    """Emails attending upon server receiving tachycardic HR post

    This server not only logs any events of tachycardic HR postings
    but also emails the attending on file for that patient. The email
    will alert the attending of the patient ID associated with the
    HR posting.

    Args:
        patient (dict): accepts patient dict containing all patient info
        att (dict): accepts attending dict containing all attending info
        email (str): accepts attending email as string

    Returns:
        int: status code returned from interaction with email server
        str: status text describing successful email or error message
    """
    path = "http://vcm-7631.vm.duke.edu:5007/hrss/send_email"
    email_subj = 'WARNING: Tachycardic HR Detected'
    att_name_list = att["name"].split('.')
    att_last_name = att_name_list[0]
    email_msg = 'Dear Dr. {},\n'
    'The HR sentinel server has just detected a tachycardic '
    'heart rate for your patient with ID {}. Please tend to '
    'them as soon as possible.'.format(att_last_name,
                                       patient["id"])
    email_req = {"from_email": "HR_sentinel@gmail.com",
                 "to_email": email,
                 "subject": email_subj,
                 "content": email_msg}
    r = requests.post(path, json=email_req)
    print(r.status_code)
    print(r.text)
    return


def prev_heart_rate(patient):
    """Gives list of all posted heart rates for a patient

    The accepted patient database is analyzed to produce a list of
    all previously posted heart rates for that patient.

    Args:
        patient (dict): accepts patient dict containing all patient info

    Returns:
        list: all heart rate values stored in specified patient database
    """
    if len(patient["HR_data"]) == 0:
        return "ERROR: no heart rate values saved for patient"
    else:
        hr_list = []
        for x in patient["HR_data"]:
            hr_list.append(x["heart_rate"])
    return hr_list


def heart_rate_average(hr_list):
    """Averages posted heart rates of a patient

    The accepted heart rate list of a specific patient is iterated
    through to produce a total which is then divided by the list
    length to produce the heart rate average.

    Args:
        hr_list (list): list of all posted heart rates of a patient

    Returns:
        int: rounded average heart rate value for a patient
    """
    total = 0
    for x in hr_list:
        total += x
    hr_avg = int(total/len(hr_list))
    return hr_avg


def heart_rate_interval(interval_time, patient):
    """Gives list of heart rates posted after a specified time

    Iterates through patient heart rate values to determine which
    heart rates were posted after the specified interval time,
    then returns a list of those heart rates to be averaged later.

    Args:
        interval_time (str): posted interval time in format
                             "Y-%m-%d %H:%M%S"
        patient (dict): accepts patient dict containing all patient info

    Returns:
        list: heart rate list containing all heart rates posted after interval
    """
    interval_dt = dt.strptime(interval_time, "%Y-%m-%d %H:%M:%S")
    hr_interval = []
    if len(patient["HR_data"]) == 0:
        return "ERROR: no heart rate values saved for patient"
    else:
        for x in patient["HR_data"]:
            hr_dt = dt.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")
            if hr_dt > interval_dt:
                hr_interval.append(x["heart_rate"])
    return hr_interval


def str_to_int(value):
    """Converts an input string
    into int value, or returns input
    if input is already int

    Args:
        value (int, str): Accepts an int or string to convert to int

    Returns:
        tuple (int, bool): returns (integer value, True) if conversion success
                           returns (-1,False)            if conversion failed
    """
    if(type(value) == int):
        return (value, True)
    try:
        int_val = int(value)
    except ValueError:
        return (-1, False)
    return (int_val, True)


if __name__ == "__main__":
    logging.basicConfig(filename='HR_sentinel_server_log.log',
                        filemode='w', level=logging.INFO)
    app.run()
