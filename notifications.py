import logging
import random
import pandas as pd
from send import send_morn_not, send_eve_not
import firebase_admin
from firebase_admin import credentials, firestore

# For testing
# cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
# usersDB = firestore.client()


def send_morning_notification(usersDB):
    # get all users tokens:
    docs = usersDB.collection("Users").stream()
    users_ref = usersDB.collection('Users')
    tokens = []
    for user in docs:
        doc_ref = users_ref.document(user.id)
        document_snapshot = doc_ref.get()
        token = document_snapshot.get('token')
        tokens.append(token)
    tokens = list(dict.fromkeys(tokens))

    # rand a sentence:
    num = random.randint(1, 50)
    daily_sentences_origin = pd.read_csv('DB/daily_sentences/tipsforhealthylife.csv')

    # send notification:
    mes = daily_sentences_origin.iloc[num]["text"]  # save text for after!
    logging.info(f"the message is: {mes}")
    send_morn_not("DAILY TIP - " + daily_sentences_origin.iloc[num]["head"],
                      "Good morning! Find the full tip in the app's chat. Open now for a positive start to your day!",
                      mes, tokens)


def send_evening_notification(usersDB):
    docs = usersDB.collection("Users").stream()
    users_ref = usersDB.collection('Users')
    tokens = []
    for user in docs:
        doc_ref = users_ref.document(user.id)
        document_snapshot = doc_ref.get()
        # todo: check if the token request works properly
        token = document_snapshot.get('token')
        tokens.append(token)
    tokens = list(dict.fromkeys(tokens))

    mes = "Don't Forget to Update Your Nutrition Diary Today!"
    logging.info(f"the message is: {mes}")
    send_eve_not(mes, tokens)


# if __name__ == '__main__':
#     send_morning_notification(usersDB)
