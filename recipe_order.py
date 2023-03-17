import requests
import json

'''def edamam_try():

    url = "https://api.edamam.com/api/recipes/v2?type=public&q=onion&app_id=3749f87d&" \
          "app_key=191597bb0eccc02907ba8e5efb98fc8b&health=fodmap-free"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    # return list of: name, picture, ingredients, prep time, calories per serving, link to the full recipe
    response = requests.request("GET", url, headers=headers)
    response_dict = json.loads(response.text)
    print(response_dict['hits'][0]['recipe']['label'])
    print(response_dict['hits'][0]['recipe']['images']['SMALL']['url'])
    print(response_dict['hits'][0]['recipe']['url'])
    print(response_dict['hits'][0]['recipe']['ingredientLines'])


class Recipe:
    def __init__(self, name, picture, ingredients, prep_time, calories_per_serving, full_recipe_link):
        self.recipe_bool = True # for using in the app to distinguish between messages
        self.name = name
        self.picture = picture
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.calories_per_serving = calories_per_serving
        self.full_recipe_link = full_recipe_link


def rapid_api_recipes_info():
    import requests

    url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"

    querystring = {"query": "italian wedding soup"}

    headers = {
        "X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
        "X-RapidAPI-Host": "recipe-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)'''


def recipe_order(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")

    # optional parameters of recipe request: Diet, Health, Meal, Food-Type (ingredients)
    meal = parameters.get("Meal")
    meal_query = ""
    if meal:
        meal_query = "&mealType=" + meal
    health = parameters.get("Health")
    health_query = ""
    if health:
        health_query = "&health=" + health # for now i allowed only one health
    diet = parameters.get("Diet")
    diet_query = ""
    if diet:
        diet_query = "&diet=" + diet # for now i allowed only one health
    #ingr = parameters.get("Food_Type")

    query_string = "https://api.edamam.com/api/recipes/v2?type=public&app_id=3749f87d&" \
          "app_key=191597bb0eccc02907ba8e5efb98fc8b" + meal_query + health_query + diet_query + "&random=true"
    print(query_string)

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    # return list of: name, picture, ingredients, prep time, calories per serving, link to the full recipe
    response = requests.request("GET", query_string, headers=headers)
    response_dict = json.loads(response.text)
    print(response_dict['hits'][0])
    #print(response_dict['hits'][0]['recipe']['label'])
    #print(response_dict['hits'][0]['recipe']['images']['SMALL']['url'])
    #print(response_dict['hits'][0]['recipe']['url'])
    #print(response_dict['hits'][0]['recipe']['ingredientLines'])

    return 'new recipe'