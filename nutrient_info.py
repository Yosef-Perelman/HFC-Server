import json

import requests

fill_text = '%20'


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
    print(food)
    query = query + food

    url = 'https://api.edamam.com/api/nutrition-data?app_id=5cb3740f&' \
          'app_key=a9e3c561a5d66e6b507a809b9b28e07b&nutrition-type=cooking' + query

    print(url)

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    # return list of: name, picture, ingredients, prep time, calories per serving, link to the full recipe
    response = requests.request("GET", url, headers=headers)
    response_dict = json.loads(response.text)
    print(response_dict)

    return response_dict['calories']