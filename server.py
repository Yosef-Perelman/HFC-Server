import json

from flask import Flask, request
import pymongo
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials, firestore

# flask
app = Flask(__name__)

# firebase
cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred)
usersDB = firestore.client()

#mongo
cluster = MongoClient("mongodb+srv://yosef:QV2NewXImbi9RCwI@cluster0.jy50tmb.mongodb.net/?retryWrites=true&w=majority")
foodDB = cluster["FoodDB"]
collection = foodDB["Food and Calories"]


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    return res


# processing the request from dialogflow
def processRequest(req):
    #sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    #query_text = result.get("queryText")
    parameters = result.get("parameters")
    #cust_name = parameters.get("cust_name")
    #cust_contact = parameters.get("cust_contact")
    #cust_email = parameters.get("cust_email")

    if intent == 'add_food_record':
        for food in parameters.get("Food_Type"):
            results = collection.find({"Food": food})
            doc_ref = usersDB.collection(u'users').document(u'yosef').collection(parameters.get("Meal"))
            doc_ref.set({
                u'name': food,
                u'calories': result["Calories"]
            })

    return {
        'fulfillmentText' : "The meal updated!"
    }


if __name__ == '__main__':
    app.run(port=5000, debug=True)