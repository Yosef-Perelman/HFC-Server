# import image_loading
# import recipe_order as ro
# import data
# import send
#
#
# def create_params(meal, health, diet, dish):
#     meal = meal
#     meal_query = ""
#     if meal:
#         print(meal)
#         meal_query = "&mealType=" + meal
#     health = health
#     health_query = ""
#     if health:
#         print(health)
#         health_query = "&health=" + health
#     diet = diet
#     diet_query = ""
#     if diet:
#         diet = ro.format_string(diet)
#         print(diet)
#         diet_query = "&diet=" + diet
#     dish = dish
#     dish_query = ""
#     if dish:
#         dish.replace(' ', '%20')
#         print(dish)
#         dish_query = "&dishType=" + dish
#
#     return meal_query, health_query, diet_query, dish_query
#
#
# # def test_api():
# #     for tag in data.health_tags:
# #         format_tag = 'DASH'
# #         if tag != 'DASH':
# #             format_tag = ro.format_string(tag)
# #         if format_tag == 'mediterranean':
# #             format_tag = 'Mediterranean'
# #
# #         meal_query, health_query, diet_query, dish_query = create_params(None, format_tag, None, None)
# #         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
# #         names = []
# #         for hit in hits:
# #             names.append(hit['recipe']['label'])
# #         print(f"label = {format_tag}.\nresponse = {names}")
# #
# #     for tag in data.diet_tags:
# #         meal_query, health_query, diet_query, dish_query = create_params(None, None, tag, None)
# #         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
# #         names = []
# #         for hit in hits:
# #             names.append(hit['recipe']['label'])
# #         print(f"label = {tag}.\nresponse = {names}")
# #
# #     for tag in data.meals:
# #         meal_query, health_query, diet_query, dish_query = create_params(tag, None, None, None)
# #         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
# #         names = []
# #         for hit in hits:
# #             names.append(hit['recipe']['label'])
# #         print(f"label = {tag}.\nresponse = {names}")
# #
# #     for tag in data.dish_types:
# #         tag.replace(' ', '%20')
# #         meal_query, health_query, diet_query, dish_query = create_params(None, None, None, tag)
# #         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
# #         hits = response['hits']
# #         names = []
# #         for hit in hits:
# #             names.append(hit['recipe']['label'])
# #         print(f"label = {tag}.\nresponse = {names}")

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
               "If you need help formulating the recipe request, you can enter the app's guide found in the main menu"
    assert recipe_order(req, usersDB, True) == error_msg


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


# def test_missing_personal_details():
#     # Write a test case with a request where fill_details_check returns False.
#     # Ensure the expected error message is returned.