
# *** imports ***

from datetime import datetime

from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore

#from add_food_record import add_food_record
from nutrient_info import food_get_info
from recipe_order import recipe_order

# *** setup ***

# flask

app = Flask(__name__)

# date
date = datetime.now().strftime("%m%d%Y")

# firebase
cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred)
usersDB = firestore.client()

# make the parameters fit to the DB
#def capitalize_words(s):
#    return ' '.join(word.capitalize() for word in s.split())


# *** code ***

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    print(req)
    # res = processRequest(req)
    # res = json.dumps(res, indent=4)
    # print(res)
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
    # cust_contact = parameters.get("cust_contact")
    # cust_email = parameters.get("cust_email")

    #if intent == 'add_food_record':
     #   return add_food_record(req)

    if intent == 'recipe.request':
        return recipe_order(req)

    if intent == 'food.get.info':
        return food_get_info(req)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    #test_firebase()
    #rapid_api_nutrition_info()
    #rapid_api_recipes_info()
    #edamam_try()