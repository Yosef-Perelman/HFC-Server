import json
import requests
import logging

import parse_parameters
from datetime import datetime


# logging
# logging.basicConfig(filename="logs/personal_details.log",
#                     format="%(asctime)s %(levelname)s %(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S",
#                     level=logging.INFO)


def calculate_age(birth_date):
    try:
        birth_date = datetime.fromisoformat(birth_date.split('T')[0])
        current_date = datetime.now().date()
        age = current_date.year - birth_date.year

        # Adjust age if the birth month and day have not yet occurred this year
        if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age
    except:
        logging.error("Error in calculate age.")
        return "error"


def get_gender(session_id, usersDB):
    logging.info("start get gender func")

    users_ref = usersDB.collection('Users')
    try:
        query_ref = users_ref.where('sessionId', '==', session_id)
        doc = next(query_ref.stream())
        doc_ref = users_ref.document(doc.id)
        document_snapshot = doc_ref.get()
        return document_snapshot.get('gender')
    except:
        logging.error("Error in getting the gender. Maybe the session isn't fit to any user in the database.")
        return "error"


def update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB):
    users_ref = usersDB.collection('Users')

    # Create a query against the collection
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    doc_ref = users_ref.document(doc.id)

    doc_ref.update({"age": age, "height": height, "weight": weight, "activity_level": activity_level,
                    "purpose": purpose_str, "daily_calories": daily_calories, "fill_details": True})


def set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB):
    logging.info("start set calorie daily func")

    gender = str(get_gender(session_id, usersDB))
    if gender == "error":
        logging.info("Error in get gender func so return error and get out from set calorie func.")
        return "An error occurred."

    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    actual_age = calculate_age(age)
    if actual_age == "error":
        return "An error occurred, Please try again. Write 'personal details' to start over."
    querystring = {"age": actual_age, "gender": gender, "height": height, "weight": weight, "activitylevel": activity_level}

    headers = {
        "X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Error with the request from the api."
                     f"the error is {e}"
                     f"The parameters of the request - age: {age}, gender: {gender}, weight: {weight}, height: {height},"
                     f"activity_level: {activity_level}.")
        return "Something is wrong with the api connection, Please try again. Write 'personal details' to start over."

    response_dict = json.loads(response.text)
    try:
        if purpose_str == 'maintain weight':
            daily_calories = response_dict['data']['goals'][purpose_str]
        else:
            daily_calories = response_dict['data']['goals'][purpose_str]['calory']
        logging.info("The daily calories: " + str(daily_calories))
        update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB)
    except Exception as e:
        return "Something is wrong with the api connection, Please try again. Write 'personal details' to start over."
    return "Very good! Your details updated, and your recommended daily calories consumption has set."


def personal_details(req, usersDB):
    logging.info("start personal details func")
    session_id, age, height, weight, activity_level, purpose_str = parse_parameters.parse_parameters(req)
    return set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB)
