import json
import requests
import parse_parameter2
from datetime import datetime

def calculate_age(birth_date):
    birth_date = datetime.fromisoformat(birth_date.split('T')[0])
    current_date = datetime.now().date()
    age = current_date.year - birth_date.year

    # Adjust age if the birth month and day have not yet occurred this year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


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
                    "purpose": purpose_str, "daily_calories": daily_calories, "fill_details": True})


def set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB):
    gender = str(get_gender(session_id, usersDB))

    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    querystring = {"age": calculate_age(age), "gender": gender, "height": height, "weight": weight, "activitylevel": activity_level}

    headers = {
        "X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_dict = json.loads(response.text)
    print(response_dict)
    if purpose_str == 'maintain weight':
        daily_calories = response_dict['data']['goals'][purpose_str]
    else:
        daily_calories = response_dict['data']['goals'][purpose_str]['calory']
    print("your daily calories: " + str(daily_calories))
    update_in_DB(session_id, age, height, weight, activity_level, daily_calories, purpose_str, usersDB)


def personal_details(req, usersDB):
    session_id, age, height, weight, activity_level, purpose_str = parse_parameter2.parse_parameters2(req)
    set_calorie_daily(session_id, age, height, weight, activity_level, purpose_str, usersDB)
    return "Good"