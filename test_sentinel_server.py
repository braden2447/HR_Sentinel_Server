import pytest
from datetime import datetime as dt
from sentinel_server import patient_database
from sentinel_server import attending_database


@pytest.mark.parametrize("input, expected", [
    (
        ({"a": 4, "b": 5, "c": "hi"}, {"a": [int], "b": [int], "c": [str]}),
        (True, 200)
    ),
    (
        ({"a": "4", "b": 5, "c": "hi"},
         {"a": [int, str], "b": [int], "c": [str]}),
        (True, 200)
    ),
    (
        ({"a": 4, "b": 5, "c": "hi"}, {"a": [str], "b": [int], "c": [str]}),
        ("The key {} has invalid data type".format("a"), 400)
    ),
    (
        ({"a": 4, "b": 5, "c": "hi"},
         {"a": [int], "b": [int], "c": [str, int]}),
        ("The value \"{}\"".format("hi") +
         " in key {} cannot be cast to int".format("c"), 400)
    ),
    (
        ({"a": 4, "b": 5, "c": "hi"},
         {"a": [int], "b": [int], "c": [str], "d": [int]}),
        ("The key {} is missing from input".format("d"), 400)
    ),
    (
        ("Potato",  {"a": [int], "b": [int], "c": [str]}),
        ("The input was not a dictionary.", 400)
    )])
def test_validate_dict_input(input, expected):
    from sentinel_server import validate_dict_input
    res1, res2 = validate_dict_input(input[0], input[1])
    assert res1 == expected[0] and res2 == expected[1]


@pytest.mark.parametrize("pat_id,  att_name, pat_age", [])
def test_add_patient_to_database(pat_id, att_name, pat_age):
    from sentinel_server import add_patient_to_database
    None


@pytest.mark.parametrize("id_no", [])
def test_get_patient_from_database(id_no):
    from sentinel_server import get_patient_from_database
    None


@pytest.mark.parametrize("att_name, att_email, att_phone", [])
def test_add_attending_to_database(att_name, att_email, att_phone):
    from sentinel_server import add_attending_to_database
    None


@pytest.mark.parametrize("attendant_name", [])
def test_get_attending_from_database(attendant_name):
    from sentinel_server import get_attending_from_database
    None


@pytest.mark.parametrize("patient, heart_rate, expected", [
    ({"id": 1, "age": 50, "HR_data": []},
     60,
     [{"heart_rate": 60, "status": "not tachycardic",
      "timestamp": (dt.now()).strftime("%Y-%m-%d %H:%M:%S")}]),
    ({"id": 2, "age": 20,
      "HR_data": [{"heart_rate": 60,
                   "status": "not tachycardic",
                   "timestamp": "2021-10-31 12:00:00"}]},
     120,
     [{"heart_rate": 60, "status": "not tachycardic",
       "timestamp": "2021-10-31 12:00:00"},
      {"heart_rate": 120, "status": "tachycardic",
       "timestamp": (dt.now()).strftime("%Y-%m-%d %H:%M:%S")}])
     ])
def test_add_heart_rate(patient, heart_rate, expected):
    from sentinel_server import add_heart_rate, is_tachycardic
    add_heart_rate(patient, heart_rate)
    answer = patient["HR_data"]
    assert answer == expected


@pytest.mark.parametrize("hr, age, expected", [
    (100, 1, "not tachycardic"),
    (160, 2, "tachycardic"),
    (100, 4, "not tachycardic"),
    (140, 3, "tachycardic"),
    (100, 6, "not tachycardic"),
    (135, 7, "tachycardic"),
    (100, 9, "not tachycardic"),
    (135, 10, "tachycardic"),
    (100, 13, "not tachycardic"),
    (120, 14, "tachycardic"),
    (90, 15, "not tachycardic"),
    (110, 50, "tachycardic")])
def test_is_tachycardic(hr, age, expected):
    from sentinel_server import is_tachycardic
    answer = is_tachycardic(hr, age)
    assert answer == expected


@pytest.mark.parametrize("patient, expected", [
    ({"id": 1, "age": 50, "HR_data": []},
     "ERROR: no heart rate values saved for patient"),
    ({"id": 2, "age": 20,
      "HR_data": [{"heart_rate": 60,
                   "status": "not tachycardic",
                   "timestamp": "2021-10-31 12:00:00"}]},
     [60]),
    ({"id": 3, "age": 40,
      "HR_data": [{"heart_rate": 60,
                   "status": "not tachycardic",
                   "timestamp": "2021-10-31 12:00:00"},
                  {"heart_rate": 120,
                   "status": "tachycardic",
                   "timestamp": "2021-10-31 18:00:00"}]},
     [60, 120])])
def test_prev_heart_rate(patient, expected):
    from sentinel_server import prev_heart_rate
    answer = prev_heart_rate(patient)
    assert answer == expected


@pytest.mark.parametrize("hr_list, expected", [
    ([60], 60),
    ([40, 40, 60, 80, 100], 64),
    ([75, 79, 82, 101], 84)])
def test_heart_rate_average(hr_list, expected):
    from sentinel_server import heart_rate_average
    answer = heart_rate_average(hr_list)
    assert answer == expected


@pytest.mark.parametrize("interval_time, patient, expected", [
    ("2020-01-01 06:00:00",
     {"id": 1, "age": 50, "HR_data": []},
     "ERROR: no heart rate values saved for patient"),
    ("2021-10-31 06:00:00",
     {"id": 2, "age": 20,
      "HR_data": [{"heart_rate": 60,
                   "status": "not tachycardic",
                   "timestamp": "2021-10-30 12:00:00"}]},
     []),
    ("2021-10-15 06:00:00",
     {"id": 3, "age": 20,
      "HR_data": [{"heart_rate": 60,
                   "status": "not tachycardic",
                   "timestamp": "2021-10-01 12:00:00"},
                  {"heart_rate": 120, "status":
                   "tachycardic",
                   "timestamp": "2021-10-20 12:00:00"},
                  {"heart_rate": 65,
                   "status": "not tachycardic",
                   "timestamp": "2021-10-31 12:00:00"}]},
     [120, 65])])
def test_heart_rate_interval(interval_time, patient, expected):
    from sentinel_server import heart_rate_interval
    answer = heart_rate_interval(interval_time, patient)
    assert answer == expected


def test_str_to_int():
    from sentinel_server import str_to_int
    None
