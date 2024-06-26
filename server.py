from flask import Flask, request
from flask_apscheduler import APScheduler
import firebase_admin
from firebase_admin import credentials, firestore, db
import logging

from meal_planer import plan_meal
from notifications import send_evening_notification, send_morning_notification
from personal_details import personal_details
from recipe_order import recipe_order
from nutrient_info import food_get_info
from get_response_id import double_check

from datetime import datetime

import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

MORNING_NOTIFICATION_TIME = 8
EVENING_NOTIFICATION_TIME = 20

# flask
app = Flask(__name__)
sched = APScheduler()

# date
date = datetime.now().strftime("%m%d%Y")

# firebase
cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
usersDB = firestore.client()

# logging
logging.basicConfig(filename="server.log",
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

# *** code ***


@app.route('/webhook', methods=['POST'])
def webhook():
    logging.error("enter webhook func")
    req = request.get_json(force=True)
    logging.info(f"request: {req}")

    if not double_check(usersDB, req):
        result = req.get("queryResult")
        intent = result.get("intent").get('displayName')
        response = process_request(req)
        return {'fulfillmentText' : response}
    return {'fulfillmentText' : "ignore"}


def process_request(req):
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')

    if intent == 'recipe.request':
        logging.info("Enter to 'recipe.request' intent")
        return recipe_order(req, usersDB)

    if intent == 'food.get.info':
        logging.info("Enter to 'food.get.info' intent")
        return food_get_info(req)

    if intent == 'meal.planning':
        logging.info("Enter to 'meal.planning' intent")
        return plan_meal(req, usersDB)

    if intent == 'personal_details':
        logging.info("Enter to 'personal_details' intent")
        return personal_details(req, usersDB)

    if intent == "test":
        logging.info("Enter to 'test' intent")
        return "server answer: test"


def morning_notification():
    logging.info('Sending morn note. The time is: %s' % datetime.now())
    send_morning_notification(usersDB)


def evening_notification():
    logging.info('Sending eve note. The time is: %s' % datetime.now())
    send_evening_notification(usersDB)


if __name__ == '__main__':
    sched.add_job(id='morning_not', func=morning_notification, trigger = 'cron', day_of_week = 'mon-sun',
                  hour = MORNING_NOTIFICATION_TIME, minute = 0)
    sched.add_job(id='evening_not', func=evening_notification, trigger='cron', day_of_week='mon-sun',
                  hour=EVENING_NOTIFICATION_TIME, minute=0)
    sched.start()
    app.run(port=5000, debug=True, use_reloader = False)

