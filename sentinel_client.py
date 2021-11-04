import requests

path = "http://127.0.0.1:5000/api"

# Test new attending route
print("Test new attending route\n")
attending1 = {"attending_username": "Smith.J",
              "attending_email": "jsmith@gmail.com",
              "attending_phone": "919-830-6608"}
r = requests.post(path + "/new_attending", json=attending1)
print(r.status_code)
print(r.text)

attending2 = {"attending_username": "McDonald.R",
              "attending_email": "notlovinit@gmail.com",
              "attending_phone": "727-888-1234"}
r = requests.post(path + "/new_attending", json=attending2)
print(r.status_code)
print(r.text)

# Test new patient route
print("Test new patient route\n")
patient1 = {"patient_id": 1,
            "attending_username": "Smith.J",
            "patient_age": 21}
r = requests.post(path + "/new_patient", json=patient1)
print(r.status_code)
print(r.text)

patient2 = {"patient_id": 2,
            "attending_username": "Smith.J",
            "patient_age": 20}
r = requests.post(path + "/new_patient", json=patient2)
print(r.status_code)
print(r.text)

patient3 = {"patient_id": 3,
            "attending_username": "McDonald.R",
            "patient_age": 65}
r = requests.post(path + "/new_patient", json=patient3)
print(r.status_code)
print(r.text)

# Test heart rate route & its subroutes
print("Test heart rate route & its subroutes\n")
pat1_hr1 = {"patient_id": 1,
            "heart_rate": 70}
r = requests.post(path + "/heart_rate", json=pat1_hr1)
print(r.status_code)
print(r.text)

pat1_hr2 = {"patient_id": 1,
            "heart_rate": 140}
r = requests.post(path + "/heart_rate", json=pat1_hr2)
print(r.status_code)
print(r.text)

pat1_hr3 = {"patient_id": 1,
            "heart_rate": 100}
r = requests.post(path + "/heart_rate", json=pat1_hr3)
print(r.status_code)
print(r.text)

# Test heart_rate/interval_average route
print("Test heart_rate/interval_average route\n")
p1_i1 = {
    "patient_id": 1,
    "heart_rate_average_since": "2018-03-09 11:00:36"
    }
r = requests.post(path + "/heart_rate/interval_average", json=p1_i1)
print(r.status_code)
print(r.text)

p1_i2 = {
    "patient_id": 1,
    "heart_rate_average_since": "2022-03-09 11:00:36"
    }
r = requests.post(path + "/heart_rate/interval_average", json=p1_i2)
print(r.status_code)
print(r.text)

p2_i2 = {
    "patient_id": 2,
    "heart_rate_average_since": "2018-03-09 11:00:36"
    }
r = requests.post(path + "/heart_rate/interval_average", json=p2_i2)
print(r.status_code)
print(r.text)


'''pat1_hr1 = {"patient_id": 1,
            "heart_rate": 70}
r = requests.post(path + "/heart_rate", json=pat1_hr1)
print(r.status_code)
print(r.text)


pat1_hr2 = {"patient_id": "1",
            "heart_rate": "120"}
r = requests.post(path + "/heart_rate", json=pat1_hr2)
print(r.status_code)
print(r.text)


# /status/<patient_id> path


x = requests.get(path + "/heart_rate/1")
print(x.status_code)
print(x.text)


x = requests.get(path + "/heart_rate/average/1")
print(x.status_code)
print(x.text)


interval1 = {"patient_id": 1,
            "heart_rate_average_since": "2020-01-01 12:00:00"}
r = requests.post(path + "/heart_rate/interval_average", json=interval1)
print(r.status_code)
print(r.text)


interval2 = {"patient_id": 1,
            "heart_rate_average_since": "2021-12-01 12:00:00"}
r = requests.post(path + "/heart_rate/interval_average", json=interval2)
print(r.status_code)
print(r.text)'''
