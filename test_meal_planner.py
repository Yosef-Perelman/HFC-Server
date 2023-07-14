# import time
# import data
# import meal_planer as mp
# import firebase_admin
# from firebase_admin import credentials, messaging, firestore
#
# cred = credentials.Certificate('hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'hfc-app-b33ed.appspot.com'})
# usersDB = firestore.client()
#
# # def test():
# #     daily_calories = 2000
# #     forbiddenfoods = ['peanuts', 'garlic']
# #     forbiddenfoods = [string.lower() for string in forbiddenfoods]
# #     dislike_recipes = ['cheesy broccoli quinoa casserole', 'better than takeout chicken fried rice',
# #                        'roasted chickpeas','man pleasing chicken',
# #                        'matzo kugel','chunky vegetable chicken spaghetti bolognaise']
# #
# #     for tag in data.health_tags:
# #         healthLabels = [tag]
# #         healthLabels = [string.lower() for string in healthLabels]
# #
# #         number_of_days = 5
# #
# #         user = mp.UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
# #         start_time = time.time()
# #         print(f"the label to search: {tag}")
# #         print("start to make the meal plan")
# #         mp.constraint_satisfaction(user, number_of_days)
# #         end_time = time.time()
# #         print("Total time:", end_time - start_time, "seconds")
# #         print(f"finish the label to search: {tag}\n")
#
#
# def test_communication():
#     daily_calories = 2000
#     forbiddenfoods = ['peanuts', 'garlic']
#     forbiddenfoods = [string.lower() for string in forbiddenfoods]
#     dislike_recipes = ['cheesy broccoli quinoa casserole', 'better than takeout chicken fried rice',
#                        'roasted chickpeas', 'man pleasing chicken',
#                        'matzo kugel', 'chunky vegetable chicken spaghetti bolognaise']
#
#     healthLabels = ['Diary-Free']
#     healthLabels = [string.lower() for string in healthLabels]
#
#     number_of_days = 3
#
#     user = mp.UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
#     start_time = time.time()
#     print(f"the label to search: Vegetarian")
#     print("start to make the meal plan")
#     session = "29bea3b2-6703-6e65-e977-375cddd6b9ff"
#     mp.constraint_satisfaction(user, number_of_days, usersDB, session)
#     end_time = time.time()
#     print("Total time:", end_time - start_time, "seconds")
#     print(f"finish the label to search: Vegetarian\n")
#
#
# if __name__ == '__main__':
#     test_communication()
import csv
import json
import random
import time

import firebase_admin
import pytest
from firebase_admin import credentials, messaging, firestore
import data
import pandas as pd

from firebase_connection import get_doc
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
    index = random.randint(0, 100)
    recipe = create_recipe(breakfast_recipes.iloc[index])
    assert hc(user, meal, recipe, []) == True


def test_constraint_satisfaction():

    file_path = 'meal_plan_algo_results1.txt'
    file = open(file_path, 'w')

    filename = 'performance_data1.csv'
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['Iteration', 'Daily Calories', 'Health Labels Number', 'Performance'])

    file.write("***************************\n")
    file.write("Test number 1: daily calories = 2000\n")

    daily_calories = 2000
    file.write(f"daily calories: {daily_calories}\n")

    counter = 1

    for tag in data.health_tags:
        tag = tag.lower()
        healthLabels = [tag]
        file.write(f"health tag: {healthLabels}\n")
        forbiddenfoods = ['peanuts', 'garlic']
        file.write(f"forbidden foods: {forbiddenfoods}\n")
        dislike_recipes = []
        file.write(f"dislike_recipes: []\n")
        user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
        number_of_days = 4
        file.write(f"number of days: 4\n")

        curr_time = time.time()
        constraint_satisfaction(user, number_of_days, test=True)
        end_time = time.time()
        file.write(f"total time: {end_time - curr_time}\n")
        writer.writerow([f'{counter}', f'{daily_calories}', f'{int(len(healthLabels))}', f'{end_time - curr_time}'])
        counter += 1

    file.write("***************************\n")
    file.write("Test number 1: daily calories = 2000\n")

    daily_calories = 3000
    file.write(f"daily calories: {daily_calories}\n")

    counter = 1

    for tag in data.health_tags:
        tag = tag.lower()
        healthLabels = [tag]
        file.write(f"health tag: {healthLabels}\n")
        forbiddenfoods = ['peanuts', 'garlic']
        file.write(f"forbidden foods: {forbiddenfoods}\n")
        dislike_recipes = []
        file.write(f"dislike_recipes: []\n")
        user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
        number_of_days = 4
        file.write(f"number of days: 4\n")

        curr_time = time.time()
        constraint_satisfaction(user, number_of_days, test=True)
        end_time = time.time()
        file.write(f"total time: {end_time - curr_time}\n")
        writer.writerow([f'{counter}', f'{daily_calories}', f'{int(len(healthLabels))}', f'{end_time - curr_time}'])
        counter += 1

    file.write("***************************\n")
    file.write("Test number 1: daily calories = 2000\n")

    daily_calories = 1000
    file.write(f"daily calories: {daily_calories}\n")

    counter = 1

    for tag in data.health_tags:
        tag = tag.lower()
        healthLabels = [tag]
        file.write(f"health tag: {healthLabels}\n")
        forbiddenfoods = ['peanuts', 'garlic']
        file.write(f"forbidden foods: {forbiddenfoods}\n")
        dislike_recipes = []
        file.write(f"dislike_recipes: []\n")
        user = UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
        number_of_days = 4
        file.write(f"number of days: 4\n")

        curr_time = time.time()
        constraint_satisfaction(user, number_of_days, test=True)
        end_time = time.time()
        file.write(f"total time: {end_time - curr_time}\n")
        writer.writerow([f'{counter}', f'{daily_calories}', f'{int(len(healthLabels))}', f'{end_time - curr_time}'])
        counter += 1

    file.close()
    csvfile.close()

#test_constraint_satisfaction()