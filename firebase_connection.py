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


def get_doc(session_id, usersDB):
    users_ref = usersDB.collection('Users')
    query_ref = users_ref.where('sessionId', '==', session_id)
    return next(query_ref.stream())


def get_token(doc):
    token = doc.to_dict().get('token')
    return [token]


def get_daily_calories(usersDB, doc):
    users_ref = usersDB.collection('Users')
    doc_ref = users_ref.document(doc.id)
    document_snapshot = doc_ref.get()
    daily_calories = document_snapshot.get('daily_calories')
    return daily_calories


def get_recipe(usersDB, name):
    return usersDB.collection('Recipes').where('name', '==', name).get()


def get_false_rated_recipes(user_name, usersDB):
    ratings_ref = usersDB.collection('Rate').where('userId', '==', user_name).where('like', '==', False)
    rated_recipes = []
    for rating in ratings_ref.stream():
        recipe_id = rating.get('recipeId')
        recipe_doc = usersDB.collection('Recipes').document(recipe_id).get()
        recipe_data = recipe_doc.to_dict()
        rated_recipes.append(recipe_data.get('title'))
    return rated_recipes
