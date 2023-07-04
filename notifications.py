import random
import pandas as pd


from send import send_notification


def sendNotifications(usersDB):
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
    mes = daily_sentences_origin.iloc[num]["text"] #save text for after!
    send_notification("DAILY TOPIC - "+daily_sentences_origin.iloc[num]["head"],"Good Morning! The daily tip is waiting for you on the chat page", "", tokens)

