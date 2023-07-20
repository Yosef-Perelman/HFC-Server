import pytest
from parse_parameters import parse_parameters, age_validation


# Test the function with a valid input
def test_parse_parameters_valid_input():
    req = {
        'queryResult': {
            'queryText': '1',
            'parameters': {
                'age': '2000-12-12T12:00:00+02:00',
                'weight': '68',
                'height': '169',
                'activity': '2',
                'goal': '1'
            },
        },
        'session': 'projects/hfc-app-378515/agent/sessions/AZiKo7j8fpFG'
    }

    session_id, age, height, weight, activity_level, purpose_str = parse_parameters(req)

    assert session_id == 'AZiKo7j8fpFG'
    assert age == '2000-12-12T12:00:00+02:00'
    assert height == '169'
    assert weight == '68'
    assert activity_level == 'level_2'
    assert purpose_str == 'maintain weight'


# Test the function with invalid or missing input
def test_parse_parameters_invalid_input():
    # Missing 'queryResult' key
    req = {
        'session': 'projects/hfc-app-378515/agent/sessions/AZiKo7j8fpFG'
    }
    with pytest.raises(Exception):
        parse_parameters(req)

    # Missing 'session' key
    req = {
        'queryResult': {
            'queryText': '1',
            'parameters': {
                'age': '2000-12-12T12:00:00+02:00',
                'weight': '68',
                'height': '169',
                'activity': '2',
                'goal': '1'
            },
        }
    }
    with pytest.raises(Exception):
        parse_parameters(req)

    # Invalid 'purpose' parameter (non-digit value)
    req = {
        'queryResult': {
            'queryText': '1',
            'parameters': {
                'age': '2000-12-12T12:00:00+02:00',
                'weight': '68',
                'height': '169',
                'activity': '2',
                'goal': 'invalid'
            },
        },
        'session': 'projects/hfc-app-378515/agent/sessions/AZiKo7j8fpFG'
    }
    with pytest.raises(Exception):
        parse_parameters(req)


def test_valid_birth_date_format():
    valid_date = '2000-12-12T12:00:00+02:00'
    assert age_validation(valid_date) == True


def test_invalid_birth_date_format():
    invalid_date = '2000-12-12 12:00:00+02:00'  # Missing 'T' separator
    assert age_validation(invalid_date) == False

    invalid_date = '2000/12/12T12:00:00+02:00'  # Invalid separator
    assert age_validation(invalid_date) == False

    invalid_date = '2000-13-12T12:00:00+02:00'  # Invalid month (13)
    assert age_validation(invalid_date) == False

    invalid_date = '2000-12-32T12:00:00+02:00'  # Invalid day (32)
    assert age_validation(invalid_date) == False

    invalid_date = '2000-12-12T25:00:00+02:00'  # Invalid hour (25)
    assert age_validation(invalid_date) == False

    invalid_date = '2000-12-12T12:60:00+02:00'  # Invalid minute (60)
    assert age_validation(invalid_date) == False
