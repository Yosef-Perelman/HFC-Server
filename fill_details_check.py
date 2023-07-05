
def fill_details_check(session_id, usersDB):
    users_ref = usersDB.collection('Users')
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    doc_ref = users_ref.document(doc.id)
    document_snapshot = doc_ref.get()
    fill_details = document_snapshot.get('fill_details')
    if not fill_details:
        return False
    return True
