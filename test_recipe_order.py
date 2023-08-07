from time import sleep

import data
from recipe_order import recipe_order
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
usersDB = firestore.client()


# def test_successful_recipe_order():
#
#     # Important note: the API allow only 10 requests in a minute
#     counter = 0
#     for label in data.health_tags:
#         if (counter % 9 == 0) & (counter != 0):
#             sleep(60)
#         health = label
#         req = {
#             "queryResult": {
#                 'parameters': {'Meal': 'Breakfast', 'Health': health, 'Dish_Type': 'desserts', 'Diet': ''}
#             },
#             "session": "projects/hfc-app-378515/agent/sessions/lUPyFyfNHdyi"
#         }
#         assert recipe_order(req, usersDB, True) is None


def test_missing_parameters():
    req = {
        "queryResult": {
            'parameters': {'Meal': '', 'Health': '', 'Dish_Type': '', 'Diet': ''}
        },
        "session": "projects/hfc-app-378515/agent/sessions/lUPyFyfNHdyi"
    }
    error_msg = "I'm sorry, but I need some specific details to find the perfect recipe for you." \
               " Please include at least one parameter such as meal type, dish type, health tag," \
               " or diet tag in your request. " \
               "If you need help formulating the recipe request, you can enter the app's guide, found in the main menu."
    assert recipe_order(req, usersDB, True) == error_msg


# test real users so the session id should be real
def test_api_request_failure():
    req = {
        "queryResult": {
            'parameters': {'Meal': 'Breakfast', 'Health': '404', 'Dish_Type': '', 'Diet': ''}
        },
        "session": "projects/hfc-app-378515/agent/sessions/lUPyFyfNHdyi"
    }
    assert recipe_order(req, usersDB, True) is None


def test_successful_recipe_order_default_dish():
    req = {
        "queryResult": {
            'parameters': {'Meal': 'Breakfast', 'Health': '', 'Dish_Type': '', 'Diet': ''}
        },
        "session": "projects/hfc-app-378515/agent/sessions/lUPyFyfNHdyi"
    }
    assert recipe_order(req, usersDB, True) is None