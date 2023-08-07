import json
import requests
import logging


fill_text = '%20'


def short_num(num):
    number = float(num)
    return "{:.2f}".format(number)


def food_get_info(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")

    # optional parameters of recipe request: Diet, Health, Meal, Food-Type (ingredients)
    query = "&ingr="
    quantity = parameters.get("quantity")
    if quantity:
        query = query + str(quantity) + fill_text
    unit = parameters.get("Unit")
    if unit:
        query = query + unit + fill_text
    food = parameters.get("food_type")
    logging.info(food)
    query = query + food

    url = 'https://api.edamam.com/api/nutrition-data?app_id=5cb3740f&' \
          'app_key=a9e3c561a5d66e6b507a809b9b28e07b&nutrition-type=cooking' + query

    logging.info(url)

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    # todo: try and catch
    # return list of: name, picture, ingredients, prep time, calories per serving, link to the full recipe
    response = requests.request("GET", url, headers=headers)
    response_dict = json.loads(response.text)
    logging.info(response_dict)

    try:
        calories = short_num(str(response_dict['totalNutrients']['ENERC_KCAL']['quantity']))
        protein = short_num(str(response_dict['totalNutrients']['PROCNT']['quantity']))
        fat = short_num(str(response_dict['totalNutrients']['FAT']['quantity']))
        carbohydrates = short_num(str(response_dict['totalNutrients']['CHOCDF']['quantity']))
        return "Name: " + response_dict['ingredients'][0]['text'] \
               + "\n\nCalories: " + calories \
               + "\nProtein: " + protein \
               + "\nFat: " + fat \
               + "\nCarbohydrates: " + carbohydrates
    except:
        return "We cannot calculate the nutrition for the ingredient. Please check the ingredient spelling." \
               "Please make sure that you entered names of ingredients and not names of dishes." \
               "If you still have a problem, enter to the app's guide for more information about this feature."
