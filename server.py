# *** imports ***
import json

import requests
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

import create_examples_in_firebase
import personal_details2
import recipe_order2
from add_exercise import add_exercise_record
from add_food_record import add_food_record
from constraint_satisfaction import from_bot
from get_false_recipes import get_false_rated_recipes
from nutrient_info import food_get_info
from personal_details import personal_details_update, more_personal_details_update
from recipe_order import recipe_order
from createDB import create_recipe_object, req

# *** setup ***

# flask
app = Flask(__name__)

# date
date = datetime.now().strftime("%m%d%Y")

# firebase
cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred)
usersDB = firestore.client()

# *** code ***

@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(force=True)
    print(req)

    response = process_request(req)
    return {
        'fulfillmentText' : response
    }


# processing the request from dialogflow
def process_request(req):
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')

    if intent == 'add.food.record':
        return add_food_record(req)

    #if intent == 'recipe.request':
    #    return recipe_order(req)

    if intent == 'recipe.request':
        return recipe_order2.recipe_order(req, usersDB)

    if intent == 'food.get.info':
        return food_get_info(req)

    profile_update = "profile - age - height - weight - activity_level - purpose"
    if intent == profile_update:
        return personal_details_update(req, usersDB)

    if intent == 'forbidden_foods - yes' or intent == 'forbidden_foods - no':
        return more_personal_details_update(req, usersDB)

    if intent == 'add.exercise.record':
        return add_exercise_record(req)

    if intent == 'meal.planning':
        return from_bot(req, usersDB)

    if intent == 'personal_details':
        return personal_details2.personal_details(req, usersDB)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    #get_false_rated_recipes(usersDB)
    #create_examples_in_firebase.create(usersDB)