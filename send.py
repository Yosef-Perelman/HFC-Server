#import firebase_admin
from firebase_admin import credentials, messaging

#cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
#firebase_admin.initialize_app(cred)


def send_tip(title, msg, registration_token, data=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data= data,
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)


def send_data(title, msg, registration_token, data=None):
    message = messaging.MulticastMessage(
        data={"request": title,
              "card": data,
              "text": msg},
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)


def send_recipe(title, msg, registration_token, recipe=None):
    message = messaging.MulticastMessage(
        data= {"request":title,"text": msg, "card": recipe},
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)


def test_send(title, msg, registration_token, data=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data= {"text":"success"},
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)

'''tokens = ["eLghHTEuQtOKN_4850QQIM:APA91bHwhBFFS3dhbhavn2MhZMTiwjsh1z6nFtoC6-jUICmYWQvulj5YFPIlCdr0o335-F5ugOJ-dq"
          "61VyJNwL_gF-a4oYaezWQWDaaT-PycF0lR1okphaj0Ousf9LpjbS5VDjG-ErnS"]
test_send("Hi", "yosefffff", tokens)'''

