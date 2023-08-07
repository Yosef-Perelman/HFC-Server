from personal_details import set_calorie_daily, get_gender, calculate_age


def test_set_calorie_daily():

    # Valid input
    assert set_calorie_daily(None, 25, 170, 70, 'level_3', 'maintain weight', test=True) == "ignore"

    # Wrong weight
    assert set_calorie_daily(None, 25, 170, 'error', 'level_3', 'maintain weight', test=True) == "ignore"

    # Wrong age
    assert set_calorie_daily(None, 'error', 170, 70, 'level_3', 'maintain weight', test=True) == "ignore"


def test_get_gender():

    # Wrong input of database connection details
    assert get_gender(None, None) == 'error'


def test_calculate_age():

    # Valid input where the age should be 22
    age = "2000-12-12T12:00:00+02:00"
    assert calculate_age(age) == 23

    # Wrong format of date
    assert calculate_age('0') == 'error'


if __name__ == '__main__':
    test_set_calorie_daily()
    test_get_gender()
    test_calculate_age()