import pytest
from sentinel_server import patient_database
from sentinel_server import attending_database

@pytest.mark.parametrize("input, expected", [])
def test_validate_dict_input(input, expected):
    from sentinel_server import validate_dict_input
    None

@pytest.mark.parametrize("input, expected", [])
def test_add_patient_to_database(pat_id, att_name, pat_age):
    from sentinel_server import add_patient_to_database
    None

@pytest.mark.parametrize("input, expected", [])
def test_get_patient_from_database(id_no):
    from sentinel_server import get_patient_from_database
    None

@pytest.mark.parametrize("input, expected", [])
def test_add_attending_to_database(att_name, att_email, att_phone):
    from sentinel_server import add_attending_to_database
    None

@pytest.mark.parametrize("input, expected", [])
def test_get_attending_from_database(attendant_name):
    from sentinel_server import get_attending_from_database
    None


def test_str_to_int(value):
    from sentinel_server import str_to_int
    None
