from personal_details import set_calorie_daily, get_gender, calculate_age


def test_set_calorie_daily():
    success_message = "Thank you on filling out your personal details! Now, let's get started and explore what you can do:\n\n" \
           "- Search Recipe: Find a variety of recipes tailored to your preferences and dietary needs.\n\n" \
           "- Ask for a Meal Plan: Get personalized meal plans based on your dietary requirements, preferences, and goals.\n\n" \
           "- Get Nutritional Information: Access nutritional information for various foods.\n\n" \
           "- Otherway, you can return to the home page and starting manage your Nutritional Diary." \
           " Your recommended daily calories consumption already there!\n\n" \
           "If you need help, you are welcome to visit the app's guide found in the main menu.\n\n" \
           "Start enjoying these features and have a great time using our app!"

    error_message = "Something is wrong with the api connection, Please try again." \
               " Make sure all the details you entered are in the correct format." \
               " Write 'personal details' to start over."

    gender_error_message = "An error occurred."

    # Valid input
    assert set_calorie_daily(None, 25, 170, 70, 'level_3', 'maintain weight', test=True) == success_message

    # Wrong weight
    assert set_calorie_daily(None, 25, 170, 'error', 'level_3', 'maintain weight', test=True) == error_message

    # Wrong height
    assert set_calorie_daily(None, 'error', 170, 70, 'level_3', 'maintain weight', test=True) == error_message

    # Wrong input for gender checking (can't connect to the firebase and get the gender)
    assert set_calorie_daily(None, 'error', 170, 70, 'level_3', 'maintain weight', test=False) == gender_error_message


def test_get_gender():

    # Wrong input of database connection details
    assert get_gender(None, None) == 'error'


def test_calculate_age():

    # Valid input where the age should be 22
    age = "2000-12-12T12:00:00+02:00"
    assert calculate_age(age) == 22

    # Wrong format of date
    assert calculate_age('0') == 'error'
