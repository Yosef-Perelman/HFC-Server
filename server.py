import json
from datetime import datetime

from flask import Flask, request
import pymongo
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials, firestore

# flask
app = Flask(__name__)

# date
date = datetime.now().strftime("%m%d%Y")

# firebase
cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred)
usersDB = firestore.client()

# mongo
cluster = MongoClient("mongodb+srv://yosef:QV2NewXImbi9RCwI@cluster0.jy50tmb.mongodb.net/?retryWrites=true&w=majority")
foodDB = cluster["FoodDB"]
collection = foodDB["Food and Calories"]


# make the parameters fit to the DB
def capitalize_words(s):
    return ' '.join(word.capitalize() for word in s.split())

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    print(req)
    # res = processRequest(req)
    processRequest(req)
    # res = json.dumps(res, indent=4)
    # print(res)
    return {
        'fulfillmentText' : "Server says: The meal updated!"
    }


# processing the request from dialogflow
def processRequest(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    # query_text = result.get("queryText")
    parameters = result.get("parameters")
    # cust_name = parameters.get("cust_name")
    # cust_contact = parameters.get("cust_contact")
    # cust_email = parameters.get("cust_email")

    if intent == 'add_food_record':
        meal = parameters.get("Meal")
        calories = 0
        for food in parameters.get("Food_Type"):
            print("food: ", food)
            food_name = capitalize_words(food)
            results = collection.find({"Food": food_name})
            for result in results:
                print(result)
                calories = result["Calories"]
            #doc_ref = usersDB.collection(u'users').document(u'eli')
            doc_ref = usersDB.collection(u'users').document(u'yosef').collection(date).document(meal).\
                collection(sessionID).document(food_name)
            #.collection(datetime.now().strftime("%m/%d/%Y")).document(parameters.get("Meal"))
            doc_ref.set({
                u'name': food_name,
                u'calories': calories
            })

    #return {'fulfillmentText' : "Server says: The meal updated!"}


'''def test_mongo():
    word = capitalize_words("tomato")
    results = collection.find({"Food": word})
    for result in results:
        print(result)
        print(result["Calories"])'''


def test_firebase():
    food_name = "Tomato"
    results = collection.find({"Food": food_name})
    for result in results:
        print(result)
        calories = result["Calories"]
    doc_ref = usersDB.collection(u'users').document(u'yosef').collection(date).collection(u'breakfast').document(u'intent_id')
    # .collection(datetime.now().strftime("%m/%d/%Y")).document(parameters.get("Meal"))
    doc_ref.set({
        u'name': food_name,
        u'calories': calories
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    #test_mongo()
    #test_firebase()