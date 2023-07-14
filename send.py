import firebase_admin
from firebase_admin import credentials, messaging, firestore
#from firebase_admin import messaging
import logging


# cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
# usersDB = firestore.client()


# def send_tip(title, msg, registration_token, data=None):
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=msg
#         ),
#         data= data,
#         tokens=registration_token,
#     )
#     response = messaging.send_multicast(message)
#     print('Successfully sent message:', response)


def send_text(title, msg, registration_token):
    logging.info(f"Trying to send text message. content: {msg}")
    message = messaging.MulticastMessage(
        data= {"request":title,"text": msg},
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    logging.info('Successfully sent message')


def send_notification(title, short_mes, message, token):
    message = messaging.MulticastMessage(
        data= {"request":"daily sentences","text": message},
        notification=messaging.Notification(
            title=title,
            body=short_mes
        ),
        tokens=token
    )
    response = messaging.send_multicast(message)


def send_morning_notification(title, short_mes, message, token):
    message = messaging.MulticastMessage(
        data= {"request":"note","text": message},
        notification=messaging.Notification(
            title=title,
            body=short_mes
        ),
        tokens=token
    )
    response = messaging.send_multicast(message)


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


# def test_send(title, msg, registration_token, data=None):
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=msg
#         ),
#         data= {"text":"success"},
#         tokens=registration_token,
#     )
#     response = messaging.send_multicast(message)
#     print('Successfully sent message:', response)

# tokens = ["eLghHTEuQtOKN_4850QQIM:APA91bHwhBFFS3dhbhavn2MhZMTiwjsh1z6nFtoC6-jUICmYWQvulj5YFPIlCdr0o335-F5ugOJ-dq"
#           "61VyJNwL_gF-a4oYaezWQWDaaT-PycF0lR1okphaj0Ousf9LpjbS5VDjG-ErnS"]
# test_send("Hi", "yosefffff", tokens)

