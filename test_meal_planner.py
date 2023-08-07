import csv
import random
import time
import data
import pandas as pd
from meal_planer import parse_parameters, UserProfile, Meal, create_recipe, hc, constraint_satisfaction


def test_parse_parameters():
    # Valid input
    parameters = {'Health': ['none'], 'Food_Type': ['none'], 'number': 5.0}
    assert parse_parameters(parameters) == (True, [], [], 5)

    # Wrong type of number
    parameters = {'Health': ['none'], 'Food_Type': ['none'], 'number': 'hi'}
    assert parse_parameters(parameters) == (False, None, None, None)

    # Number as int and not a float
    parameters = {'Health': ['none'], 'Food_Type': ['none'], 'number': 5}
    assert parse_parameters(parameters) == (True, [], [], 5)

    # Health that didn't in the healthLabels list
    parameters = {'Health': ['none', 'test'], 'Food_Type': ['none'], 'number': 5.0}
    assert parse_parameters(parameters) == (True, [], [], 5)


def test_hard_constraints():
    daily_calories = 2000
    healthLabels = ['vegetarian']
    forbiddenfoods = ['peanuts', 'garlic']
    dislike_recipes = ['cheesy broccoli quinoa casserole', 'better than takeout chicken fried rice',
                       'roasted chickpeas','man pleasing chicken',
                       'matzo kugel','chunky vegetable chicken spaghetti bolognaise']
    user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
    meal = Meal(None, 'breakfast')
    breakfast_recipes_origin = pd.read_csv('DB/filtered with images/breakfast.csv')
    breakfast_recipes = breakfast_recipes_origin.sample(frac=1)
    breakfast_recipes = breakfast_recipes.reset_index(drop=True)
    index = random.randint(1, 100)
    recipe = create_recipe(breakfast_recipes.iloc[index])
    assert isinstance(hc(user, meal, recipe, []), bool)


def test_constraint_satisfaction():

    daily_calories = 2000
    for tag in data.health_tags:
        tag = tag.lower()
        healthLabels = [tag]
        forbiddenfoods = ['peanuts', 'garlic']
        dislike_recipes = []
        user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
        number_of_days = 4
        response = constraint_satisfaction(user, number_of_days, test=True)
        assert len(response) == 12


# def test_performance_calories():
#     print('starting')
#     file_path = 'meal_plan_algo_results_CALORIES.txt'
#     file = open(file_path, 'w')
#
#     filename = 'performance_data_CALORIES.csv'
#     csvfile = open(filename, 'w', newline='')
#     writer = csv.writer(csvfile)
#     writer.writerow(['Iteration', 'Daily Calories', 'Health Label', 'Time Performance', 'Number Of Meals'])
#
#     forbiddenfoods = ['peanuts', 'garlic']
#     file.write(f"forbidden foods: {forbiddenfoods}\n")
#     dislike_recipes = []
#     file.write(f"dislike_recipes: []\n")
#     number_of_days = 4
#     file.write(f"number of days: 4\n")
#
#     file.write('\n')
#     file.write("***************************\n")
#     print('starting first test')
#     file.write("Test number 1: daily calories = 2000\n")
#
#     daily_calories = 2000
#
#     counter = 1
#
#     for tag in data.health_tags:
#         tag = tag.lower()
#         healthLabels = [tag]
#         file.write(f"health tag: {healthLabels}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}'])
#         print(f'{counter} finish tag')
#         counter += 1
#         file.write('\n')
#
#     file.write("***************************\n")
#     print('starting second test')
#     file.write("Test number 2: daily calories = 3000\n")
#
#     daily_calories = 3000
#
#     for tag in data.health_tags:
#         tag = tag.lower()
#         healthLabels = [tag]
#         file.write(f"health tag: {healthLabels}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.write("***************************\n")
#     print('starting theard test')
#     file.write("Test number 3: daily calories = 1000\n")
#
#     daily_calories = 1000
#
#     for tag in data.health_tags:
#         tag = tag.lower()
#         healthLabels = [tag]
#         file.write(f"health tag: {healthLabels}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.close()
#     csvfile.close()
#
#
# def test_performance_health_labels():
#     print('starting')
#     file_path = 'meal_plan_algo_results_HEALTH_LABELS.txt'
#     file = open(file_path, 'w')
#
#     filename = 'performance_data_HEALTH_LABELS.csv'
#     csvfile = open(filename, 'w', newline='')
#     writer = csv.writer(csvfile)
#     writer.writerow(
#         ['Iteration', 'Daily Calories', 'Health Labels', 'Time Performance', 'Number Of Meals', 'Number Of Parameters'])
#
#     daily_calories = 2000
#     file.write(f"daily_calories: {daily_calories}\n")
#
#     counter = 1
#
#     dislike_recipes = []
#     file.write(f"dislike_recipes: []\n")
#     number_of_days = 4
#     file.write(f"number of days: 4\n")
#     forbiddenfoods = ['peanuts', 'garlic']
#     file.write(f"forbidden foods: {forbiddenfoods}\n")
#
#     file.write('\n')
#     file.write("***************************\n")
#     print('starting first test')
#     file.write("Test number 1: one health labels\n")
#
#     for i in range(10):
#         chosen_strings = random.sample(data.health_tags, 1)
#         healthLabels = []
#         for tag in chosen_strings:
#             healthLabels.append(tag.lower())
#         file.write(f"health tags: {healthLabels}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         number_of_parameters = 3
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}',
#              f'{number_of_parameters}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.write("***************************\n")
#     print('starting second test')
#     file.write("Test number 2: three health labels\n")
#
#     for i in range(10):
#         chosen_strings = random.sample(data.health_tags, 3)
#         healthLabels = []
#         for tag in chosen_strings:
#             healthLabels.append(tag.lower())
#         file.write(f"health tags: {healthLabels}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         number_of_parameters = 5
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}',
#              f'{number_of_parameters}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.write("***************************\n")
#     print('starting third test')
#     file.write("Test number 3: five health labels\n")
#
#     for i in range(10):
#         chosen_strings = random.sample(data.health_tags, 5)
#         healthLabels = []
#         for tag in chosen_strings:
#             healthLabels.append(tag.lower())
#         file.write(f"health tags: {healthLabels}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         number_of_parameters = 7
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}',
#              f'{number_of_parameters}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.close()
#     csvfile.close()
#
#
# def test_performance_forbidden_foods():
#     print('starting')
#     file_path = 'meal_plan_algo_results_FORB_FOODS.txt'
#     file = open(file_path, 'w')
#
#     filename = 'performance_data_FORB_FOODS.csv'
#     csvfile = open(filename, 'w', newline='')
#     writer = csv.writer(csvfile)
#     writer.writerow(['Iteration', 'Daily Calories', 'Forbidden Foods', 'Time Performance', 'Number Of Meals',
#                      'Number Of Parameters'])
#
#     daily_calories = 2000
#     file.write(f"daily_calories: {daily_calories}\n")
#
#     counter = 1
#     foods = ['peanuts', 'garlic', 'apple', 'cheese', 'onion', 'bread', 'chocolate', 'tomato', 'potato']
#
#     dislike_recipes = []
#     file.write(f"dislike_recipes: []\n")
#     number_of_days = 4
#     file.write(f"number of days: 4\n")
#     healthLabels = []
#     file.write(f"health tags: {healthLabels}\n")
#
#     file.write('\n')
#     file.write("***************************\n")
#     print('starting first test')
#     file.write("Test number 1: three forbidden foods\n")
#
#     for i in range(10):
#         chosen_strings = random.sample(foods, 3)
#         forbiddenfoods = []
#         for tag in chosen_strings:
#             forbiddenfoods.append(tag)
#         file.write(f"forbidden foods: {forbiddenfoods}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         number_of_parameters = 3
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{forbiddenfoods}', f'{end_time - curr_time}', f'{response_len}',
#              f'{number_of_parameters}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.write("***************************\n")
#     print('starting second test')
#     file.write("Test number 2: six health labels\n")
#
#     for i in range(10):
#         chosen_strings = random.sample(foods, 6)
#         forbiddenfoods = []
#         for tag in chosen_strings:
#             forbiddenfoods.append(tag)
#         file.write(f"forbidden foods: {forbiddenfoods}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         number_of_parameters = 6
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}',
#              f'{number_of_parameters}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.write("***************************\n")
#     print('starting third test')
#     file.write("Test number 3: nine health labels\n")
#
#     for i in range(10):
#         forbiddenfoods = []
#         for tag in foods:
#             forbiddenfoods.append(tag)
#         file.write(f"forbidden foods: {forbiddenfoods}\n")
#         user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#
#         curr_time = time.time()
#         result = constraint_satisfaction(user, number_of_days, test=True)
#         end_time = time.time()
#         if result is None:
#             response_len = 0
#         else:
#             response_len = int(len(result))
#         file.write(f'output length: {response_len}\n')
#         file.write(f"total time: {end_time - curr_time}\n")
#         number_of_parameters = 9
#         writer.writerow(
#             [f'{counter}', f'{daily_calories}', f'{healthLabels}', f'{end_time - curr_time}', f'{response_len}',
#              f'{number_of_parameters}'])
#         counter += 1
#         print(f'{counter} finish tag')
#         file.write('\n')
#
#     file.close()
#     csvfile.close()