import json
import time

import requests
import logging
import send

import parse_parameters
from datetime import datetime
from firebase_connection import get_doc, get_token

DEFAULT_AGE = 30


def calculate_age(birth_date):
    try:
        birth_date = datetime.fromisoformat(birth_date.split('T')[0])
        current_date = datetime.now().date()
        age = current_date.year - birth_date.year

        # Adjust age if the birth month and day have not yet occurred this year
        if age < 0:
            age = DEFAULT_AGE

        logging.info(f"actual age = {age}")
        return age
    except:
        logging.error("Error in calculate age.")
        return "error"


def get_gender(session_id, usersDB):
    logging.info("start get gender func")
    try:
        users_ref = usersDB.collection('Users')
        query_ref = users_ref.where('sessionId', '==', session_id)
        doc = next(query_ref.stream())
        doc_ref = users_ref.document(doc.id)
        document_snapshot = doc_ref.get()
        return document_snapshot.get('gender')
    except:
        logging.error("Error in getting the gender. Maybe the session isn't fit to any user in the database.")
        return "error"


def update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB):
    try:
        users_ref = usersDB.collection('Users')
        # Create a query against the collection
        query_ref = users_ref.where('sessionId', '==', session_id)
        doc = next(query_ref.stream())
        doc_ref = users_ref.document(doc.id)

        doc_ref.update({"age": age, "height": height, "weight": weight, "activity_level": activity_level,
                        "purpose": purpose_str, "daily_calories": daily_calories, "fill_details": True})
    except:
        logging.error("Error in updating the database.")
        return "error"


def set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB=None, test=False):
    logging.info("start set calorie daily func")

    # if not test:

    if not test:
        doc = get_doc(session_id, usersDB)
        tokens = get_token(doc)
        gender = str(get_gender(session_id, usersDB))
        if gender == "error":
            logging.info("Error in get gender func so return error and get out from set calorie func.")
            text = "An error occurred, Please try again. Write 'personal details' to start over."
            send.send_text("text", text, tokens)
            return "ignore"
    else:
        gender = "male"

    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    if not test:
        actual_age = calculate_age(age)
        if actual_age == "error":
            text = "An error occurred, Please try again. Write 'personal details' to start over."
            send.send_text("text", text, tokens)
            return "ignore"

    else:
        actual_age = age

    querystring = {"age": actual_age, "gender": gender, "height": height, "weight": weight, "activitylevel": activity_level}

    headers = {
        "X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except Exception as e:
        logging.error(f"Error with the request from the api."
                     f"the error is {e}"
                     f"The parameters of the request - age: {age}, gender: {gender}, weight: {weight}, height: {height},"
                     f"activity_level: {activity_level}.")
        text = "Something is wrong with the api connection, Please try again." \
               "Make sure all the details you entered are in the correct format.\n\n" \
               " Write 'personal details' to start over."
        if not test:
            send.send_text("text", text, tokens)
        return "ignore"

    response_dict = json.loads(response.text)
    try:
        if purpose_str == 'maintain weight':
            daily_calories = response_dict['data']['goals'][purpose_str]
        else:
            daily_calories = response_dict['data']['goals'][purpose_str]['calory']
        logging.info("The daily calories: " + str(daily_calories))
        if not test:
            update_response = update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB)
            if update_response == 'error':
                text = "Can't update the database, please try again."
                if not test:
                    send.send_text("text", text, tokens)
                return "ignore"
    except Exception as e:
        text = "Something is wrong with the api connection, Please try again." \
               " Make sure all the details you entered are in the correct format." \
               " Write 'personal details' to start over."
        if not test:
            send.send_text("text", text, tokens)
        return "ignore"

    #Send the message directly to app
    text = "Thank you on filling out your personal details! Now, let's get started and explore what you can do:\n\n" \
           "- Search Recipe: Find a variety of recipes tailored to your preferences and dietary needs.\n\n" \
           "- Ask for a Meal Plan: Get personalized meal plans based on your dietary requirements, preferences, and goals.\n\n" \
           "- Get Nutritional Information: Access nutritional information for various foods.\n\n" \
           "- Otherway, you can return to the home page and starting manage your Nutritional Diary." \
           " Your recommended daily calories consumption already there!\n\n" \
           "If you need help, you are welcome to visit the app's guide found in the main menu.\n\n" \
           "Start enjoying these features and have a great time using our app!"
    if not test:
        send.send_text("text", text, tokens)
    return "ignore"


def personal_details(req, usersDB):
    start = time.time()
    logging.info("start personal details func")
    session_id = req.get("session").split('/')[-1]
    doc = get_doc(session_id, usersDB)
    tokens = get_token(doc)
    try:
        session_id, age, height, weight, activity_level, purpose_str = parse_parameters.parse_parameters(req)
    except:
        text =  "Something is wrong with the input parameters, please try again.\n" \
               " Make sure all the details you entered are in the correct format." \
               " Write 'personal details' to start over."
        send.send_text("text", text, tokens)
        return "ignore"
    response = set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB)
    end = time.time()
    logging.info(f"the time of personal details func is {str(end - start)}")
    return response
