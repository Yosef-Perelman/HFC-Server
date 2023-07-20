import logging
import random
import pandas as pd
from send import send_notification


def send_notifications(usersDB):
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
    mes = daily_sentences_origin.iloc[num]["text"] # save text for after!
    logging.info(f"the message is: {mes}")
    send_notification("DAILY TIP - " + daily_sentences_origin.iloc[num]["head"],
                      "Good morning! Find the full tip in the app's chat. Open now for a positive start to your day!",
                      mes, tokens)
