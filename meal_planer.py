import ast
import json
import time
import pandas as pd

import data
import send
import logging
from fill_details_check import fill_details_check

# logging
# logging.basicConfig(filename="logs/meal_planer.log",
#                     format="%(asctime)s %(levelname)s %(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S",
#                     level=logging.INFO)


class UserProfile:
    def __init__(self, health, forbidden_ingredients, recommended_calories, dislike_recipes):
        self.health = health
        self.forbidden_ingredients = forbidden_ingredients
        self.recommended_calories = recommended_calories
        self.dislike_recipes = dislike_recipes


class Meal:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.recipe = None


class Recipe:
    def __init__(self, name, link, picture, dietLabels, healthLabels, calories, fat, carbs, protein, ingredients):
        self.name = name
        self.full_recipe_link = link
        self.picture = picture
        self.dietLabels = dietLabels
        self.healthLabels = healthLabels
        self.ingredients = ingredients
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.protein = protein


def create_card(recipe):
    card = {'title': recipe.name,
            'image': recipe.picture,
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


def get_false_rated_recipes(user_name, usersDB):

    ratings_ref = usersDB.collection('Rate').where('userId', '==', user_name).where('like', '==', False)
    rated_recipes = []
    for rating in ratings_ref.stream():
        recipe_id = rating.get('recipeId')
        recipe_doc = usersDB.collection('Recipes').document(recipe_id).get()
        recipe_data = recipe_doc.to_dict()
        rated_recipes.append(recipe_data.get('title'))

    return rated_recipes


def create_recipe(row):
    diet = ast.literal_eval(row[3])
    health = ast.literal_eval(row[4])
    ingredients = ast.literal_eval(row[9])
    return Recipe(row[0], row[1], row[2], diet, health, row[5], row[6], row[7], row[8], ingredients)


def hc(user_profile, meal, recipe, already_chosen):

    recipe_calories = float(recipe.calories)
    user_calories = (user_profile.recommended_calories)
    if meal.type == 'breakfast':
        if recipe_calories > (user_calories / 3):
            return False
    if meal.type == 'lunch':
        if recipe_calories > (user_calories / 2):
            return False

    if recipe.name in user_profile.dislike_recipes:
        return False

    if recipe.name in already_chosen:
        return False

    if user_profile.health:
        recipe_healthLabels = [string.lower() for string in recipe.healthLabels]
        if not all(word in recipe_healthLabels for word in user_profile.health):
            return False

    if user_profile.forbidden_ingredients:
        recipe_ingredients = [string.lower() for string in recipe.ingredients]
        for food in user_profile.forbidden_ingredients:
            if food in recipe_ingredients:
                return False

    return True


def count_unique_and_duplicates(list1, list2, list3):

    combined_list = list1 + list2 + list3
    unique_set = set(combined_list)
    unique_list = list(unique_set)
    num_duplicates = sum(combined_list.count(value) > 1 for value in unique_list)
    return len(unique_list), num_duplicates


def sc(user_profile, recipe, current_assign):
    deviation = abs(float(current_assign[0].recipe.calories) + float(current_assign[1].recipe.calories) +
                    float(recipe.calories) - user_profile.recommended_calories) / 100
    unique_ingredients, duplicate_ingredients = count_unique_and_duplicates(current_assign[0].recipe.ingredients,
                                                                            current_assign[1].recipe.ingredients,
                                                                            recipe.ingredients)
    variation = duplicate_ingredients / unique_ingredients / 10
    return deviation + variation


def constraint_satisfaction(user, number_of_days, usersDB, session_id, test = False):
#def constraint_satisfaction(user, number_of_days):
    logging.info("start constraint satisfaction func")

    final_solution = []
    already_chosen_names = []
    finish = False  # finish = var that inform that the search over

    # breakfast_recipes_origin = pd.read_csv('DB/mini_breakfast.csv')
    # lunch_recipes_origin = pd.read_csv('DB/mini_lunch.csv')
    # dinner_recipes_origin = pd.read_csv('DB/mini_dinner.csv')

    # breakfast_recipes_origin = pd.read_csv('DB/test/breakfast_test.csv')
    # lunch_recipes_origin = pd.read_csv('DB/test/lunch_test.csv')
    # dinner_recipes_origin = pd.read_csv('DB/test/dinner_test.csv')

    breakfast_recipes_origin = pd.read_csv('DB/filtered with images/breakfast.csv')
    lunch_recipes_origin = pd.read_csv('DB/filtered with images/lunch.csv')
    dinner_recipes_origin = pd.read_csv('DB/filtered with images/dinner.csv')

    #breakfast_recipes_origin = pd.read_csv('DB/filtered/filtered_breakfast.csv')
    #lunch_recipes_origin = pd.read_csv('DB/filtered/filtered_lunch.csv')
    #dinner_recipes_origin = pd.read_csv('DB/filtered/filtered_dinner.csv')

    breakfast_recipes = breakfast_recipes_origin.sample(frac=1)
    lunch_recipes = lunch_recipes_origin.sample(frac=1)
    dinner_recipes = dinner_recipes_origin.sample(frac=1)

    breakfast_recipes = breakfast_recipes.reset_index(drop=True)
    lunch_recipes = lunch_recipes.reset_index(drop=True)
    dinner_recipes = dinner_recipes.reset_index(drop=True)

    start_time = time.time()

    for i in range(number_of_days):

        # end_time = time.time()
        # logging.info(f"checking the time condition. time = {end_time - start_time}")
        # if end_time - start_time > 60:
        #     logging.warning("the 60 seconds over, the search stopped")
        #     break

        if finish:
            break

        #print("start day: " + str(i + 1))
        current_assignment = [Meal(0, 'breakfast'), Meal(1, 'lunch'), Meal(2, 'dinner')]

        upper_bound = 100
        breakfast_index = 0
        lunch_index = 0
        dinner_index = 0

        end = False # var that inform that the search for the current day is over
        flag = False # var that inform that the search for the current day need to jump to the end

        while not end:

            end_time = time.time()
            logging.info(f"checking the time condition. time = {end_time - start_time}")
            if end_time - start_time > 60:
                logging.warning("the 60 seconds over, the search stopped")
                finish = True
                break

            # logging.info("starting new loop in the while loop")
            for ass in current_assignment:
                # logging.info("starting new level in the current_assignment loop")

                if flag:
                    flag = False
                    break

                if ass.type == 'breakfast':
                    while True:
                        #print(f"breakfast index: {breakfast_index}")
                        if breakfast_index < len(breakfast_recipes):
                            recipe = create_recipe(breakfast_recipes.iloc[breakfast_index])
                            if hc(user, ass, recipe, already_chosen_names):
                                ass.recipe = recipe
                                breakfast_index += 1
                                break
                            else:
                                breakfast_recipes.drop(index=breakfast_index, inplace=True)
                                #breakfast_index += 1
                                breakfast_recipes.reset_index(drop=True, inplace=True)
                        else:
                            #print("finish the breakfast index")
                            flag = True
                            end = True
                            if current_assignment[2].recipe is None:
                                finish = True
                            else:
                                names = [meal.recipe.name for meal in current_assignment]
                                #print(f"finish day {i}, find {names[0]}, {names[1]}, {names[2]},")
                                already_chosen_names.extend(names)
                                final_solution.extend(current_assignment)
                            break
                    continue

                if ass.type == 'lunch':
                    while True:
                        #print(f"lunch index: {lunch_index}")
                        if lunch_index < len(lunch_recipes):
                            recipe = create_recipe(lunch_recipes.iloc[lunch_index])
                            if hc(user, ass, recipe, already_chosen_names):
                                ass.recipe = recipe
                                lunch_index += 1
                                break
                            else:
                                lunch_recipes.drop(index=lunch_index, inplace=True)
                                #lunch_index += 1
                                lunch_recipes.reset_index(drop=True, inplace=True)
                        else:
                            #print("finish the lunch index")
                            lunch_index = 0
                            flag = True
                            break
                    continue

                if ass.type == 'dinner':
                    while True:
                        #print(f"dinner index: {dinner_index}")
                        if dinner_index < len(dinner_recipes):
                            recipe = create_recipe(dinner_recipes.iloc[dinner_index])
                            if hc(user, ass, recipe, already_chosen_names):
                                lower_bound = sc(user, recipe, current_assignment)
                                if lower_bound < upper_bound:
                                    upper_bound = lower_bound
                                    if upper_bound < 2:
                                        ass.recipe = recipe
                                        names = [meal.recipe.name for meal in current_assignment]
                                        logging.info(f"finish day {i}, find {names[0]}, {names[1]}, {names[2]},")
                                        already_chosen_names.extend(names)
                                        final_solution.extend(current_assignment)
                                        dinner_index = 0
                                        lunch_index = 0
                                        breakfast_index = 0
                                        end = True
                                        break
                                    else:
                                        ass.recipe = recipe
                                        dinner_index += 1
                                else:
                                    dinner_index += 1
                            else:
                                dinner_recipes.drop(index=dinner_index, inplace=True)
                                #dinner_index += 1
                                dinner_recipes.reset_index(drop=True, inplace=True)
                        else:
                            #print("finish the dinner index")
                            dinner_index = 0
                            breakfast_index -= 1
                            break

    cards = []
    text = f"This is the result of meal plan for {number_of_days} days.\nthe input was: " \
           f"health labels = {user.health}, forbidden foods = {user.forbidden_ingredients}."

    if not test:
        users_ref = usersDB.collection('Users')
        query_ref = users_ref.where('sessionId', '==', session_id)
        doc = next(query_ref.stream())
        token = doc.to_dict().get('token')
        tokens = [token]

    if final_solution:
        logging.info("****************")
        logging.info(text)
        day_calories = 0
        for index, value in enumerate(final_solution):

            cards.append(create_card(value.recipe))
            recipe_check = usersDB.collection('Recipes').where('name', '==', value.recipe.name).get()
            if len(recipe_check) == 0:
                data = {
                    'title': value.recipe.name,
                    'image': value.recipe.picture,
                    'url': value.recipe.full_recipe_link,
                    'calories': value.recipe.calories,
                    'healthLabels': value.recipe.healthLabels,
                    'dietLabels': value.recipe.dietLabels,
                    'ingredients': value.recipe.ingredients,
                    'fat': value.recipe.fat,
                    'protein': value.recipe.protein,
                    'carbs': value.recipe.carbs
                }
                usersDB.collection('Recipes').add(data)

            if index % 3 == 0:
                if index != 0:
                    logging.info("calories of the day:" + str(day_calories))
                    logging.info("************")
                day_calories = 0
                logging.info("day number" + str(int(index / 3) + 1) + ":")
            logging.info("recipe name: " + value.recipe.name)
            logging.info("recipe health labels:")
            logging.info(value.recipe.healthLabels)
            logging.info("recipe ingredients:")
            logging.info(value.recipe.ingredients)
            day_calories += value.recipe.calories
        logging.info("calories of the day:" + str(day_calories))
        logging.info("************\n")

        if not test:
            # todo: add checking for how many days their results and if it fit the request
            send.send_text("text", text, tokens)
            length = len(cards)
            for i in range(length):
                send.send_meal_plan("meal_plan", str(length), str(i + 1), tokens, cards[i])

    else:
        if not test:
            send.send_text("text", text, tokens)
            # send.send_text("no meal plan", "I apologize, but we couldn't find a suitable meal plan based on your preferences."
            #                " Please try adjusting your preferences or consider exploring individual recipes instead."
            #                " Need help formulating your request? Check out our guide in the main menu for instructions.",
            #                tokens)
            send.send_text("text",
                           "I apologize, but we couldn't find a suitable meal plan based on your preferences."
                           " Please try adjusting your preferences or consider exploring individual recipes instead."
                           " Need help formulating your request? Check out our guide in the main menu for instructions.",
                           tokens)


def plan_meal(req, usersDB):
    logging.info("start plan meal func")
    session_id = req.get("session").split('/')[-1]

    if not fill_details_check(session_id, usersDB):
        logging.info("Failed in fill details check")
        return "You didn't filled your personal details. Please enter to the chat-bot and do it." \
               "You can do it by writing 'personal details'."
    logging.info("Passed fill details check")

    users_ref = usersDB.collection('Users')
    query_ref = users_ref.where('sessionId', '==', session_id)
    doc = next(query_ref.stream())
    dislike_recipes = get_false_rated_recipes(doc.id, usersDB)

    # token = doc.to_dict().get('token')
    # text = "Generating your meal plan. This may take some time. Please wait."
    # tokens = [token]
    # send.send_text("text", text, tokens)

    doc_ref = users_ref.document(doc.id)
    document_snapshot = doc_ref.get()
    daily_calories = document_snapshot.get('daily_calories')
    print(f"daily calories: {daily_calories}")

    result = req.get("queryResult")
    parameters = result.get("parameters")
    healthLabels = parameters.get('Health')
    for label in healthLabels:
        if label not in data.health_tags:
            logging.warning(f"the label {label} isn't in data.health_tags")
            healthLabels.remove(label)
    healthLabels = [string.lower() for string in healthLabels]
    forbiddenfoods = parameters.get('Food_Type')
    forbiddenfoods = [string.lower() for string in forbiddenfoods]
    if forbiddenfoods[0] == "none":
        forbiddenfoods.clear()
    number_of_days = int(parameters.get('number'))

    user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
    start_time = time.time()
    print("start to make the meal plan")
    constraint_satisfaction(user, number_of_days, usersDB, session_id)
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds")

    return "finish"


