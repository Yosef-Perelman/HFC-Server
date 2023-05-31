

def get_false_rated_recipes(usersDB):
    user_name = 'kn9MUrNTtiAwQwAPWLY0'

    ratings_ref = usersDB.collection('Rate').where('userId', '==', user_name).where('like', '==', True)
    rated_recipes = []
    for rating in ratings_ref.stream():
        recipe_id = rating.get('recipeId')
        recipe_doc = usersDB.collection('Recipes').document(recipe_id).get()
        recipe_data = recipe_doc.to_dict()
        rated_recipes.append(recipe_data)

    for i in rated_recipes:
        print(i)

