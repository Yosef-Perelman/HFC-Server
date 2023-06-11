import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
firebase_admin.initialize_app(cred)

def sendPush(title, msg, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data= {"text":"data"},
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


tokens = ["eLghHTEuQtOKN_4850QQIM:APA91bHwhBFFS3dhbhavn2MhZMTiwjsh1z6nFtoC6-jUICmYWQvulj5YFPIlCdr0o335-F5ugOJ-dq61VyJNw"
          "L_gF-a4oYaezWQWDaaT-PycF0lR1okphaj0Ousf9LpjbS5VDjG-ErnS"]
sendPush("Hi", "yosefffff", tokens)

