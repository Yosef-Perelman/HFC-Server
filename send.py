import firebase_admin
from firebase_admin import messaging, credentials, firestore
import logging


# cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
# usersDB = firestore.client()


def send_text(title, msg, registration_token):
    logging.info(f"Trying to send text message. content: {msg}")
    message = messaging.MulticastMessage(
        data= {"request":title,"text": msg},
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    logging.info('Successfully sent message')


def send_morn_not(title, short_mes, message, token):
    message = messaging.MulticastMessage(
        data= {"request":"note","text": message},
        notification=messaging.Notification(
            title=title,
            body=short_mes
        ),
        tokens=token
    )
    response = messaging.send_multicast(message)
    logging.info('Successfully sent message')


def send_eve_not(title, token):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body="Tap here to enter to the diary!"
        ),
        tokens=token
    )
    response = messaging.send_multicast(message)
    logging.info('Successfully sent message')


def send_meal_plan(title, messagesNumber, currentMessage, registration_token, recipe):
    logging.info(f"Trying to send meal plan message. current message number: {currentMessage}")
    message = messaging.MulticastMessage(
        data={"request": title,
              "messagesNumber": messagesNumber,
              "currentMessage": currentMessage,
              "card": recipe
              },
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    logging.info('Successfully sent message')


def send_recipe(title, msg, registration_token, recipe):
    logging.info(f"Trying to send recipe message.")
    message = messaging.MulticastMessage(
        data= {"request":title,"text": msg, "card": recipe},
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    logging.info('Successfully sent message')

