[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/BME547-Fall2021/heart-rate-sentinel-server-anuj-braden/blob/main/LICENSE.txt)
![GitHub Actions Status](https://github.com/BME547-Fall2021/heart-rate-sentinel-server-anuj-braden/actions/workflows/pytest_runner.yml/badge.svg)

# Heart Rate Sentinel Server Project

## Authors: Braden Garrison and Anuj Som

## Due: 11/3/21

## Program Instructions:

This Flask web server functions as a simple, centralized heart rate sentinel server.
POST requests can be made to post data such as new attendings, new patients, and new heart rate data.
GET requests can be made to obtain specific information such as existing patients in database and heart rate data for each patient.
Embedded within the server are functionalities such as logging and emailing attendings when a tachycardic heart rate is posted for a patient.

This server is running on a virtual machine with the following hostname and port:

```vcm-23156.vm.duke.edu:5000```

## Server Specifications

Upon simply accessing the server without specifying an end route, the server will display a message stating:

```The server is on.```

To utilize the functions of this server, it is important that the user first adds a new attending before adding a patient that is assigned to that attending.
A new attending can be posted using the following end route:

```/api/new_attending```

The json request should be a dictionary with the format shown below:

```
{"attending_username": "Smith.J", 
 "attending_email": "dr_user_id@yourdomain.com",
 "attending_phone": "###-###-###"}
```

Subsequently, a new patient can be posted using the following end route:

```/api/new_patient```

The json request should be a dictionary with the format shown below:

```
{"patient_id": 1,
 "attending_username": "Smith.J",
 "patient_age": 25}
```

Once at least one attending and one corresponding patient have been registered into each database, new patient heart rates can be posted. 
These posted heart rates are saved within the entry of their corresponding patient under the key "HR_info".
The server will process each heart rate posting and save the heart rate value, a timestamp associated with the posting, and a  tachycardic/not tachycardic status.
A new heart rate can be posted using the following end route: and json request as a dictionary as formatted below:

```/api/heart_rate```

The json request should be a dictionary with the format shown below:

```
{"patient_id": 1,
 "heart_rate": 75}
```


GET requests can be made to the following variable URL end routes to return certain information.

To return a list of all previous heart rate measurements for an existing patient, access the following URL
with the specific patient ID number in place of <patient_id>:

```/api/heart_rate/<patient_id>```

To return an integer value for a patient's average heart rate across all stored heart rate measurements, access 
the following URL with the specific patient ID number in place of <patient_id>:

```/api/heart_rate/average/<patient_id>```

To return a detailed list of patients that a specific attending is responsible for, access the following URL
with the attending username (in format "Smith.J") in place of <attending_username>:

```/api/patients/<attending_username>```


Lastly, a POST request can also be made to return a heart rate interval average for a specific patient
after a specified time. This POST request should be made to the end route:

```/api/heart_rate/interval_average```

The json request should be a dictionary with the following format:

```
{"patient_id": 1,
 "heart_rate_average_since": "2018-03-09 11:00:36"}
```

## Server Errors

Proper POST and GET requests will be met by the specified returned values and a status code of 200.
In the event that the user tries to POST a json request with invalid dictionary formatting/keys or 
tries to obtain data via GET request of a non-existing patient, a corresponding error message will be returned 
with a status code of 400.