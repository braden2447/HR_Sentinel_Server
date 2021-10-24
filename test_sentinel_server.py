import pytest
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


def test_str_to_int():
    from sentinel_server import str_to_int
    None
