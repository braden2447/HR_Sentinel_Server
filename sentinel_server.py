from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


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
        "patient_age": int,         # in years
    }
    Method will validate input and post valid patient information
    to server

    Returns:
        dict: patient dictionary added to database
    """
    return None, 500


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
        "attending_phone": str      # Phone #, ###-###-####
    }
    This method will be used to match information to an existing attending,
    as specified by the new_patient() method
    
    Returns:
        dict: attending dict added to database
    """
    return None, 500


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """Accepts json request and posts new patient
    to server database.

    Method curated by _______

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
    return None, 500


@app.route("/api/status/<patient_id>", methods=["GET"])
def status_pid(patient_id):
    """Accepts json request and posts new patient
    to server database.

    Method curated by _______

    <patient_id> request should contain an existing pid.
    The output will return a json dict formatted as follows:
    {
        "heart_rate": int,
        "status":  str ("tachycardic" | "not tachycardic"),
        "timestamp": str ("2018-03-09 11:00:36")
    }
    This method will be used to tell if specified patient
    is tachycardic or not, and the time of the most recent
    heart rate
    
    Returns:
        string: Status
    """
    return None, 500


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate_pid(patient_id):
    return None, 500


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_avg_pid(patient_id):
    return None, 500


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def heart_rate_interval_avg():
    return None, 500


@app.route("/api/patients/<attending_username>", methods=["GET"])
def patients_attending_username(attending_username):
    return None, 500


if __name__ == "__main__":
    app.run()
