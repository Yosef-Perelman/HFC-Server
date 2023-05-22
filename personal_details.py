import json
import requests

from parse_parameter_profile import parse_parameters1, parse_parameters2


def get_gender(session_id, usersDB):
    users_ref = usersDB.collection('Users')

    # Create a query against the collection
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    doc_ref = users_ref.document(doc.id)
    document_snapshot = doc_ref.get()
    return document_snapshot.get('gender')


def update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB):
    users_ref = usersDB.collection('Users')

    # Create a query against the collection
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    doc_ref = users_ref.document(doc.id)

    doc_ref.update({"age": age, "height": height, "weight": weight, "activity_level": activity_level,
                    "purpose": purpose_str, "daily_calories": daily_calories})


def set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB):
    gender = str(get_gender(session_id, usersDB))

    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    querystring = {"age": age, "gender": gender, "height": height, "weight": weight, "activitylevel": activity_level}

    headers = {
        "X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_dict = json.loads(response.text)
    if purpose_str == 'Maintain weight':
        daily_calories = response_dict['data']['goals'][purpose_str]
    else:
        daily_calories = response_dict['data']['goals'][purpose_str]['calory']
    print("your daily calories: " + str(daily_calories))
    update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB)


def personal_details_update(req, usersDB):
    session_id, age, height, weight, activity_level, purpose_str = parse_parameters1(req)
    set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB)
    return "Good. did you have a health label?"


def more_personal_details_update(req, usersDB):
    session_id, healthLabels, forbiddenfoods = parse_parameters2(req)
    print(healthLabels)
    print(forbiddenfoods)
    users_ref = usersDB.collection('Users')

    # Create a query against the collection
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    doc_ref = users_ref.document(doc.id)

    doc_ref.update({"healthLabels": healthLabels, "forbiddenfoods": forbiddenfoods, "fill_details": "True"})