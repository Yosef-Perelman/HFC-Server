# import recipe_order as ro
# import data
# import send
#
#
# def create_params(meal, health, diet, dish):
#     meal = meal
#     meal_query = ""
#     if meal:
#         print(meal)
#         meal_query = "&mealType=" + meal
#     health = health
#     health_query = ""
#     if health:
#         print(health)
#         health_query = "&health=" + health
#     diet = diet
#     diet_query = ""
#     if diet:
#         diet = ro.format_string(diet)
#         print(diet)
#         diet_query = "&diet=" + diet
#     dish = dish
#     dish_query = ""
#     if dish:
#         dish.replace(' ', '%20')
#         print(dish)
#         dish_query = "&dishType=" + dish
#
#     return meal_query, health_query, diet_query, dish_query
#
#
# def test_api():
#     for tag in data.health_tags:
#         format_tag = 'DASH'
#         if tag != 'DASH':
#             format_tag = ro.format_string(tag)
#         if format_tag == 'mediterranean':
#             format_tag = 'Mediterranean'
#
#         meal_query, health_query, diet_query, dish_query = create_params(None, format_tag, None, None)
#         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
#         names = []
#         for hit in hits:
#             names.append(hit['recipe']['label'])
#         print(f"label = {format_tag}.\nresponse = {names}")
#
#     for tag in data.diet_tags:
#         meal_query, health_query, diet_query, dish_query = create_params(None, None, tag, None)
#         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
#         names = []
#         for hit in hits:
#             names.append(hit['recipe']['label'])
#         print(f"label = {tag}.\nresponse = {names}")
#
#     for tag in data.meals:
#         meal_query, health_query, diet_query, dish_query = create_params(tag, None, None, None)
#         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
#         names = []
#         for hit in hits:
#             names.append(hit['recipe']['label'])
#         print(f"label = {tag}.\nresponse = {names}")
#
#     for tag in data.dish_types:
#         tag.replace(' ', '%20')
#         meal_query, health_query, diet_query, dish_query = create_params(None, None, None, tag)
#         response = ro.api_request(meal_query, health_query, diet_query, dish_query)
#         hits = response['hits']
#         names = []
#         for hit in hits:
#             names.append(hit['recipe']['label'])
#         print(f"label = {tag}.\nresponse = {names}")
#
#
# def test():
#
#     usersDB = send.usersDB
#     session_id = "29bea3b2-6703-6e65-e977-375cddd6b9ff"
#     meal_query, health_query, diet_query, dish_query = create_params("breakfast", "vegetarian", None, None)
#     response = ro.api_request(meal_query, health_query, diet_query, dish_query)
#
#     recipes = ro.parse_recipes_from_api(response['hits'])
#     recipe = ro.choose_recipe(recipes, "29bea3b2-6703-6e65-e977-375cddd6b9ff", usersDB)
#
#     print(recipe.name)
#
#     recipe_check = usersDB.collection('Recipes').where('name', '==', recipe.name).get()
#     if len(recipe_check) == 0:
#         dta = {
#             'title': recipe.name,
#             'image': recipe.picture,
#             'url': recipe.full_recipe_link,
#             'calories': recipe.calories,
#             'healthLabels': recipe.healthLabels,
#             'dietLabels': recipe.dietLabels,
#             'ingredients': recipe.ingredients,
#             'fat': recipe.fat,
#             'protein': recipe.protein,
#             'carbs': recipe.carbs
#         }
#         usersDB.collection('Recipes').add(dta)
#
#     users_ref = usersDB.collection('Users')
#     # get the user name by the session_id
#     query_ref = users_ref.where('sessionId', '==', session_id)
#     doc = next(query_ref.stream())
#     token = doc.to_dict().get('token')
#
#     tokens = [token]
#     card = ro.create_card(recipe)
#     send.send_recipe("recipe", "Are you satisfied with this recipe?", tokens, card)
#
#
# if __name__ == '__main__':
#     test()