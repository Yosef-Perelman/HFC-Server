import logging
import time


def double_check(users_db, req):
    now = time.time()
    response_id = req.get('responseId')
    session_id = req.get("session").split('/')[-1]
    users_ref = users_db.collection('Users')
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    doc_ref = users_ref.document(doc.id)
    document_snapshot = doc_ref.get()
    try:
        id = document_snapshot.get('last_response_id')
    except Exception:
        doc_ref.update({'last_response_id': response_id})
        end = time.time()
        logging.info(f"finish double check. time is: {end - now}")
        logging.info(f"the response id is different, the request is new")
        return False
    if response_id == id:
        end = time.time()
        logging.info(f"finish double check. time is: {end - now}")
        logging.info(f"the response id is equal, the request isn't new")
        return True
    doc_ref.update({'last_response_id': response_id})
    end = time.time()
    logging.info(f"finish double check. time is: {end - now}")
    logging.info(f"the response id is different, the request is new")
    return False