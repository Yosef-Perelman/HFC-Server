import time
import data
import meal_planer as mp


def test():
    daily_calories = 2000
    forbiddenfoods = ['peanuts', 'garlic']
    forbiddenfoods = [string.lower() for string in forbiddenfoods]
    dislike_recipes = ['cheesy broccoli quinoa casserole', 'better than takeout chicken fried rice',
                       'roasted chickpeas','man pleasing chicken',
                       'matzo kugel','chunky vegetable chicken spaghetti bolognaise']

    for tag in data.health_tags:
        healthLabels = [tag]
        healthLabels = [string.lower() for string in healthLabels]

        number_of_days = 5

        user = mp.UserProfile(healthLabels, forbiddenfoods, daily_calories, dislike_recipes)
        start_time = time.time()
        print(f"the label to search: {tag}")
        print("start to make the meal plan")
        mp.constraint_satisfaction(user, number_of_days)
        end_time = time.time()
        print("Total time:", end_time - start_time, "seconds")
        print(f"finish the label to search: {tag}\n")


if __name__ == '__main__':
    test()