import requests
import json


class Recipe:
    def __init__(self, name, picture, link, High_Protein, Low_Carb, Low_Fat, Dairy_Free, egg_free,
                 fodmap_free, gluten_free, keto_freindly, kosher, low_sugar, paleo, peanut_free,
                 soy_free, vegan, vegetarian, ingredientLines, fat, carbs, protein, ingredients,
                 calories_per_serving, meal_type):
        #self.recipe_bool = True # for using in the app to distinguish between messages
        self.id
        self.name = name
        self.picture = picture
        self.full_recipe_link = link
        self.High_Protein = High_Protein
        self.Low_Carb = Low_Carb
        self.Low_Fat = Low_Fat
        self.Dairy_Free = Dairy_Free
        self.egg_free = egg_free
        self.fodmap_free = fodmap_free
        self.gluten_free = gluten_free
        self.keto_freindly = keto_freindly
        self.kosher = kosher
        self.low_sugar = low_sugar
        self.paleo = paleo
        self.peanut_free = peanut_free
        self.soy_free = soy_free
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.ingredientLines = ingredientLines
        self.ingredients = ingredients
        self.calories_per_serving = calories_per_serving
        self.fat = fat
        self.carbs = carbs
        self.protein = protein
        self.meal_type = meal_type



def recipe_order(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")

    # optional parameters of recipe request: Diet, Health, Meal, Food-Type (ingredients)
    meal = parameters.get("Meal")
    meal_query = ""
    if meal:
        print(meal)
        meal_query = "&mealType=" + meal
    health = parameters.get("Health")
    health_query = ""
    if health:
        print(health)
        health_query = "&health=" + health # for now i allowed only one health
    diet = parameters.get("Diet")
    diet_query = ""
    if diet:
        print(diet)
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

    return response_dict['hits'][0]['recipe']['label']

def create_recipe_object():
    # optional parameters of recipe request: Diet, Health, Meal, Food-Type (ingredients)
    meal = "breakfast"
    meal_query = ""
    if meal:
        #print(meal)
        meal_query = "&mealType=" + meal
    query_string = "https://api.edamam.com/api/recipes/v2?type=public&app_id=3749f87d&" \
                   "app_key=191597bb0eccc02907ba8e5efb98fc8b" + meal_query + "&random=true"
    #print(query_string)

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    # return list of: name, picture, ingredients, prep time, calories per serving, link to the full recipe
    response = requests.request("GET", query_string, headers=headers)
    response_dict = json.loads(response.text)

    hits = response_dict['hits']
    for i in hits:
        name = i['recipe']['label']
        picture = i['recipe']['images']['SMALL']['url']
        link = i['recipe']['url']
        dietLabels = i['recipe']['dietLabels']
        healthLabels = i['recipe']['healthLabels']
        ingredientLines = i['recipe']['ingredientLines']
        meal_type = i['recipe']['mealType']
        ingredients = i['recipe']['ingredients']
        ingredientsList = ""
        for j in ingredients:
            ingredientsList = ingredientsList + j['food'] + ' '
        totalNutrients = i['recipe']['totalNutrients']
        calories = totalNutrients['ENERC_KCAL']['quantity'] / 4
        fat = totalNutrients['FAT']['quantity'] / 4
        carbs = totalNutrients['CHOCDF']['quantity'] / 4
        sugar = totalNutrients['SUGAR']['quantity'] / 4
        protein = totalNutrients['PROCNT']['quantity'] / 4

        print('name: ')
        print(name)
        print('picture: ')
        print(picture)
        print('link: ')
        print(link)
        print('dietLabels: ')
        print(dietLabels)
        print('healthLabels: ')
        print(healthLabels)
        print('ingredientLines: ')
        print(ingredientLines)
        print('meal_type: ')
        print(meal_type)
        print('calories: ')
        print(calories)
        print('fat: ')
        print(fat)
        print('carbs: ')
        print(carbs)
        print('sugar: ')
        print(sugar)
        print('protein: ')
        print(protein)
        print('ingredient: ')
        print(ingredientsList)
        print('********************************\n')
    #print(response_dict['hits'][0])
    # print(response_dict['hits'][0]['recipe']['label'])
    # print(response_dict['hits'][0]['recipe']['images']['SMALL']['url'])
    # print(response_dict['hits'][0]['recipe']['url'])
    # print(response_dict['hits'][0]['recipe']['ingredientLines'])