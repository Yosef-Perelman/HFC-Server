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