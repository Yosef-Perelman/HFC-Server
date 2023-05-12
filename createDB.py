import requests
import json
import csv
import time

servings = 5


def create_recipe_object():
    file = open('dinner.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(["Id", "name", "picture", "link", "dietLabels", "healthLabels", "ingredientLines",
                         "meal_type", "dish_type", "calories", "fat", "carbs", "sugar", "protein", "ingredients",
                         "rate"])
    file.close()

    # optional parameters of recipe request: Diet, Health, Meal, Food-Type (ingredients)
    meal = "dinner"
    meal_query = ""
    if meal:
        meal_query = "&mealType=" + meal
    query_string = "https://api.edamam.com/api/recipes/v2?type=public&app_id=3749f87d&" \
                   "app_key=191597bb0eccc02907ba8e5efb98fc8b" + meal_query + "&dishType=Main%20course&random=true"

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    counter = 0
    times = 0
    while counter < 25:

        if times != 0 and times % 9 == 0:
            time.sleep(60)
        times += 1
        # return list of: name, picture, ingredients, prep time, calories per serving, link to the full recipe
        response = requests.request("GET", query_string, headers=headers)
        response_dict = json.loads(response.text)

        hits = response_dict['hits']

        file = open('dinner.csv', mode='a', newline='', encoding='utf-8')
        writer = csv.writer(file)

        for i in hits:

            meal_type = i['recipe']['mealType']
            if meal_type[0] == 'snack' or meal_type[0] == 'teatime':
                break
            dish_type = i['recipe']['dishType']
            if 'alcohol cocktail' in dish_type or 'drinks' in dish_type:
                break
            name = i['recipe']['label']
            picture = i['recipe']['images']['SMALL']['url']
            link = i['recipe']['url']
            dietLabels = i['recipe']['dietLabels']
            healthLabels = i['recipe']['healthLabels']
            ingredientLines = i['recipe']['ingredientLines']
            ingredients = i['recipe']['ingredients']
            ingredientsList = ""
            for j in ingredients:
                ingredientsList = ingredientsList + j['food'] + ', '
            totalNutrients = i['recipe']['totalNutrients']
            calories = totalNutrients['ENERC_KCAL']['quantity'] / servings
            fat = totalNutrients['FAT']['quantity'] / servings
            carbs = totalNutrients['CHOCDF']['quantity'] / servings
            sugar = totalNutrients['SUGAR']['quantity'] / servings
            protein = totalNutrients['PROCNT']['quantity'] / servings
            rate = "None"

            writer.writerow([counter, name, picture, link, dietLabels, healthLabels, ingredientLines,
                         meal_type, dish_type, calories, fat, carbs, sugar, protein, ingredientsList,
                         rate])

            counter += 1
        file.close()

    print("counter: ")
    print(counter)
















'''print('name: ')
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
            print('dish_type: ')
            print(dish_type)
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
            print('ingredients: ')
            print(ingredientsList)
            print('********************************\n')'''