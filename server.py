# *** imports ***
import json

import requests
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

from add_exercise import add_exercise_record
from add_food_record import add_food_record
from nutrient_info import food_get_info
from recipe_order import recipe_order
from createDB import create_recipe_object
from set_calorie_program import set_calorie_daily


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
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    # query_text = result.get("queryText")
    parameters = result.get("parameters")
    # cust_name = parameters.get("cust_name")

    if intent == 'add.food.record':
        return add_food_record(req)

    if intent == 'recipe.request':
        #return "yes"
        return recipe_order(req)

    if intent == 'food.get.info':
        return food_get_info(req)

    daily_calorie_intent_name = 'calorie.program.set - bot - age - gender - weight - height - final'
    if intent == daily_calorie_intent_name:
        return set_calorie_daily(req)

    if intent == 'add.exercise.record':
        return add_exercise_record(req)


if __name__ == '__main__':
    #app.run(port=5000, debug=True)
    #create_recipe_object()
    pass