from flask import Flask, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
cluster = MongoClient("mongodb+srv://yosef:QV2NewXImbi9RCwI@cluster0.jy50tmb.mongodb.net/?retryWrites=true&w=majority")
db = cluster["FoodDB"]
collection = db["Food and Calories"]


@app.route('/')
def add_meal():
    return 0


# getting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    print(req)

    results = collection.find({"Food" : "Tomato"})
    for result in results:
        print(result)

    return {
        'fulfillmentText' : result["Calories"]
    }


if __name__ == '__main__':
    app.run(port=5000, debug=True)