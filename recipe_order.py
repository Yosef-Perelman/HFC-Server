import random
import numpy as np
import requests
import json

import data as dta
import image_loading
import send
import logging

# logging
# logging.basicConfig(filename="logs/recipe_order.log",
#                     format="%(asctime)s %(levelname)s %(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S",
#                     level=logging.INFO)

SERVINGS = 5


class Recipe:
    def __init__(self, name, picture, link, healthLabels, dietLabels, fat, carbs,  protein, ingredients, calories):
        self.name = name
        self.picture = picture
        self.full_recipe_link = link
        self.healthLabels = healthLabels
        self.dietLabels = dietLabels
        self.ingredients = ingredients
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.protein = protein


def parse_recipes_from_DB(results):
    recipes = []
    for recipe in results:
        name = recipe["title"]
        image = recipe["image"]
        url = recipe["url"]
        health = recipe["healthLabels"]
        diet = recipe["dietLabels"]
        #health = recipe["healtlabels"]
        #diet = recipe["dietlabels"]
        fat = recipe["fat"]
        carbs = recipe["carbs"]
        protein = recipe["protein"]
        ing = recipe["ingredients"]
        cal = recipe["calories"]
        recipes.append(Recipe(name,image,url,health,diet,fat,carbs,protein,ing,cal))
    return recipes


def parse_recipes_from_api(hits):
    recipes = []
    for recipe in hits:
        name = recipe['recipe']['label']
        try:
            picture = recipe['recipe']['images']['LARGE']['url']
        except:
            picture = recipe['recipe']['images']['REGULAR']['url']
        link = recipe['recipe']['url']
        dietLabels = recipe['recipe']['dietLabels']
        healthLabels = recipe['recipe']['healthLabels']
        ingredients = recipe['recipe']['ingredients']
        ingredientsList = []
        for j in ingredients:
            ingredientsList.append(j['food'])
        totalNutrients = recipe['recipe']['totalNutrients']
        calories = totalNutrients['ENERC_KCAL']['quantity'] / SERVINGS
        fat = totalNutrients['FAT']['quantity'] / SERVINGS
        carbs = totalNutrients['CHOCDF']['quantity'] / SERVINGS
        protein = totalNutrients['PROCNT']['quantity'] / SERVINGS
        recipes.append(Recipe(name,picture,link,healthLabels,dietLabels,fat,carbs,protein,ingredientsList,calories))
    return recipes


def get_liked_recipes(session_id, usersDB):
    users_ref = usersDB.collection('Users')
    # get the user name by the session_id
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    # get the recipes that the user liked
    ratings_ref = usersDB.collection('Rate').where('userId', '==', doc.id).where('like', '==', True)
    rated_recipes = []
    for rating in ratings_ref.stream():
        recipe_id = rating.get('recipeId')
        recipe_doc = usersDB.collection('Recipes').document(recipe_id).get()
        recipe_data = recipe_doc.to_dict()
        rated_recipes.append(recipe_data)

    user_recipes = parse_recipes_from_DB(rated_recipes)

    unique_user_dietLabels = list(set(dietLabel for recipe in user_recipes for dietLabel in recipe.dietLabels))
    unique_user_healthLabels = list(set(healthLabel for recipe in user_recipes for healthLabel in recipe.healthLabels))
    unique_user_ingredients = list(set(ingredient for recipe in user_recipes for ingredient in recipe.ingredients))
    return unique_user_dietLabels, unique_user_healthLabels, unique_user_ingredients


def create_user_vector(unique_user_dietLabels, unique_user_healthLabels, unique_user_ingredients,
                       unique_ingredients, unique_healthLabels, unique_dietLabels):
    dietLabels_vector = np.zeros(len(unique_dietLabels))
    for dietLabel in unique_dietLabels:
        if dietLabel in unique_user_dietLabels:
            dietLabel_index = unique_dietLabels.index(dietLabel)
            dietLabels_vector[dietLabel_index] = 1

    healthLabels_vector = np.zeros(len(unique_healthLabels))
    for healthLabel in unique_healthLabels:
        if healthLabel in unique_user_healthLabels:
            healthLabel_index = unique_healthLabels.index(healthLabel)
            healthLabels_vector[healthLabel_index] = 1

    ingredients_vector = np.zeros(len(unique_ingredients))
    for ingredient in unique_ingredients:
        if ingredient in unique_user_ingredients:
            ingredient_index = unique_ingredients.index(ingredient)
            ingredients_vector[ingredient_index] = 1

    return np.concatenate((ingredients_vector, healthLabels_vector, dietLabels_vector))


def create_recipe_vector(recipe, unique_ingredients, unique_healthLabels, unique_dietLabels):
    dietLabels_vector = np.zeros(len(unique_dietLabels))
    for dietLabel in recipe.dietLabels:
        dietLabel_index = unique_dietLabels.index(dietLabel)
        dietLabels_vector[dietLabel_index] = 1

    healthLabels_vector = np.zeros(len(unique_healthLabels))
    for healthLabel in recipe.healthLabels:
        healthLabel_index = unique_healthLabels.index(healthLabel)
        healthLabels_vector[healthLabel_index] = 1

    ingredients_vector = np.zeros(len(unique_ingredients))
    for ingredient in recipe.ingredients:
        ingredient_index = unique_ingredients.index(ingredient)
        ingredients_vector[ingredient_index] = 1

    return np.concatenate((ingredients_vector, healthLabels_vector, dietLabels_vector))


def select_item_with_probabilities(items):
    probabilities = [0.5, 0.3, 0.2]
    rand_num = random.random()
    cumulative_prob = 0

    for item, prob in zip(items, probabilities):
        cumulative_prob += prob
        if rand_num < cumulative_prob:
            return item


def choose_recipe(recipes, session_id, usersDB):
    unique_user_dietLabels, unique_user_healthLabels, unique_user_ingredients = get_liked_recipes(session_id, usersDB)
    unique_dietLabels = list(set(dietLabel for recipe in recipes for dietLabel in recipe.dietLabels))
    unique_healthLabels = list(set(healthLabel for recipe in recipes for healthLabel in recipe.healthLabels))
    unique_ingredients = list(set(ingredient for recipe in recipes for ingredient in recipe.ingredients))
    user_preferences_vector = create_user_vector(unique_user_dietLabels, unique_user_healthLabels,
                                                 unique_user_ingredients, unique_ingredients,
                                                 unique_healthLabels, unique_dietLabels)

    similarity_scores = []
    for recipe in recipes:
        recipe_vector = create_recipe_vector(recipe, unique_ingredients, unique_healthLabels, unique_dietLabels)
        similarity_score = np.dot(user_preferences_vector, recipe_vector) / (
                np.linalg.norm(user_preferences_vector) * np.linalg.norm(recipe_vector))
        similarity_scores.append(similarity_score)

    sorted_recipes = sorted(zip(recipes, similarity_scores), key=lambda x: x[1], reverse=True)
    sorted_recipes = [recipe for recipe, _ in sorted_recipes]

    selected_item = select_item_with_probabilities(sorted_recipes)
    return selected_item


def create_card(recipe, image):
    card = {'title': recipe.name,
            'image': image,
            'url': recipe.full_recipe_link,
            'calories': recipe.calories,
            'healthLabels': recipe.healthLabels,
            'dietLabels': recipe.dietLabels,
            'ingredients': recipe.ingredients,
            'fat': recipe.fat,
            'protein': recipe.protein,
            'carbs': recipe.carbs
            }
    return json.dumps(card)


def format_string(input_string):
    formatted_string = input_string.lower().replace(' ', '-')
    return formatted_string


def api_request(meal_query, health_query, diet_query, dish_query):
    query_string = "https://api.edamam.com/api/recipes/v2?type=public&app_id=3749f87d&" \
                   "app_key=191597bb0eccc02907ba8e5efb98fc8b" + meal_query + health_query + diet_query + dish_query + "&random=true"
    print(query_string)

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    response = requests.request("GET", query_string, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict


def recipe_order(req, usersDB):
    session_id = req.get("session").split('/')[-1]

    # users_ref = usersDB.collection('Users')
    # # todo check if he fill details
    # # Create a query against the collection
    # query_ref = users_ref.where('sessionId', '==', session_id)
    # doc = next(query_ref.stream())
    # token = doc.to_dict().get('token')
    # text = "Searching for your perfect recipe. Please wait."
    # tokens = [token]
    # send.send_text("text", text, tokens)

    result = req.get("queryResult")
    parameters = result.get("parameters")

    meal = parameters.get("Meal")
    if meal not in dta.meals:
        meal = None
    meal_query = ""
    if meal:
        print(meal)
        meal_query = "&mealType=" + meal
    health = parameters.get("Health")
    if health not in dta.health_tags:
        health = None
    health_query = ""
    if health:
        print(health)
        if health != 'DASH':
            health = format_string(health)
        if health == 'mediterranean':
            health = 'Mediterranean'
        health_query = "&health=" + health
    diet = parameters.get("Diet")
    if diet not in dta.diet_tags:
        diet = None
    diet_query = ""
    if diet:
        diet = format_string(diet)
        print(diet)
        diet_query = "&diet=" + diet
    dish = parameters.get("Dish_Type")
    if dish not in dta.dish_types:
        dish = None
    dish_query = ""
    if dish:
        dish.replace(' ', '%20')
        print(dish)
        dish_query = "&dishType=" + dish

    response_dict = api_request(meal_query, health_query, diet_query, dish_query)

    recipes = parse_recipes_from_api(response_dict['hits'])
    recipe = choose_recipe(recipes, session_id, usersDB)

    print(recipe.name)

    image = image_loading.download_image(recipe.picture, recipe.name)

    recipe_check = usersDB.collection('Recipes').where('name', '==', recipe.name).get()
    if len(recipe_check) == 0:
        data = {
            'title': recipe.name,
            'image': image,
            'url': recipe.full_recipe_link,
            'calories': recipe.calories,
            'healthLabels': recipe.healthLabels,
            'dietLabels': recipe.dietLabels,
            'ingredients': recipe.ingredients,
            'fat': recipe.fat,
            'protein': recipe.protein,
            'carbs': recipe.carbs
        }
        usersDB.collection('Recipes').add(data)

    users_ref = usersDB.collection('Users')
    # get the user name by the session_id
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    token = doc.to_dict().get('token')

    tokens = [token]
    card = create_card(recipe, image)
    send.send_recipe("recipe", "Are you satisfied with this recipe?", tokens, card)

    return None


