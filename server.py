
# *** imports ***

from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

from meal_planer import plan_meal
from personal_details import personal_details
from recipe_order import recipe_order
from nutrient_info import food_get_info


# *** setup ***

# flask
app = Flask(__name__)

# date
date = datetime.now().strftime("%m%d%Y")

# firebase
cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
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


def process_request(req):
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')

    if intent == 'recipe.request':
        return recipe_order(req, usersDB)

    if intent == 'food.get.info':
        return food_get_info(req)

    if intent == 'meal.planning':
        return plan_meal(req, usersDB)

    if intent == 'personal_details':
        return personal_details(req, usersDB)


if __name__ == '__main__':
    app.run(port=5000, debug=True)