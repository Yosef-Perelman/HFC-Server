"""
variables = M1,...,M15 - all the meals in the plan
values = all the recipes in the database
hard constraints = all the preliminary requirements of the user
soft constraints = recommended daily intake of calories of the user
"""

import math
import csv


class Recipe:
    def __init__(self, id, name, picture, link, healthLabels, dietLabels,
                 ingredientLines, fat, carbs, sugar, protein, ingredients,
                 calories, meal_type, rate):
        self.id = id
        self.name = name
        self.picture = picture
        self.full_recipe_link = link
        self.healthLabels = healthLabels
        self.dietLabels = dietLabels
        self.ingredientLines = ingredientLines
        self.ingredients = ingredients
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.sugar = sugar
        self.protein = protein
        self.meal_type = meal_type
        self.rate = rate


class Meal:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.recipe = None


class UserProfile:
    def __init__(self, diet, health, forbidden_ingredients, recommended_calories):
        self.diet = diet
        self.health = health
        self.forbidden_ingredients = forbidden_ingredients
        self.recommended_calories = recommended_calories


def hc(user_profile, meal, recipe, current_assign):

    if user_profile.diet is not None:
        if user_profile.diet not in recipe.dietLabels:
            return False

    if user_profile.health is not None:
        if user_profile.health not in recipe.healthLabels:
            return False

    if user_profile.forbidden_ingredients is not None:
        for i in user_profile.forbidden_ingredients:
            if i in recipe.ingredients:
                return False
    return True

    # todo: add the constraint that the recipe didn't chosen yet

    if meal.type == 'breakfast':
        if float(recipe.calories) > (user_profile.recommended_calories / 3):
            return False
    if meal.type == 'lunch':
        if float(recipe.calories) > (user_profile.recommended_calories / 2):
            return False


# todo - edit this function if necessary
def count_unique_and_duplicates(list1, list2, list3):
    # Combine all three lists into a single list
    combined_list = list1 + list2 + list3

    # Create a set of unique values
    unique_set = set(combined_list)

    # Convert the set back to a list with no duplicates
    unique_list = list(unique_set)

    # Count the number of values that appear more than once
    num_duplicates = sum(combined_list.count(value) > 1 for value in unique_list)

    return len(unique_list), num_duplicates


def sc(user_profile, recipe, current_assign):
    deviation = abs(current_assign[0].recipe.calories + current_assign[1].recipe.calories +
                    recipe.calories - user_profile.recommended_calories) / 100
    if deviation <= 0.5:
        return 0
    unique_ingredients, duplicate_ingredients = count_unique_and_duplicates(current_assign[0].recipe.ingredients,
                                                                            current_assign[1].recipe.ingredients,
                                                                            recipe.ingredients)
    variation = duplicate_ingredients / unique_ingredients / 2
    return variation + deviation


def new_branch(var):
    pass


def next_var():
    pass


def next_val():
    pass


'''**********************************'''


def get_csv_row(filename, row_num):
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if i == row_num + 1:
                return row
    return None


def create_recipe(row):
    return Recipe(row[0], row[1], row[2], row[3], row[5], row[4], row[6], row[10], row[11], row[12],
                  row[13], row[14], row[9], row[7], row[15])


def constraint_satisfaction(current_asign, user):

    breakfast_index = 1
    lunch_index = 1
    dinner_index = 1

    for ass in current_asign:
        if ass.type == 'breakfast':
            filename = 'DB/breakfast.csv'
            index = breakfast_index
        elif ass.type == 'lunch':
            filename = 'DB/lunch.csv'
            index = lunch_index
        else:
            filename = 'DB/dinner.csv'
            index = dinner_index
        file = open(filename, 'r', encoding='utf8')
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            if i == index:
                recipe = create_recipe(row)
                if hc(user,ass,recipe,current_asign):
                    ass.recipe = recipe
                    index += 1
                    break
                else:
                    index += 1

    print(current_asign[0].recipe.name + ", " + current_asign[1].recipe.name + ", " + current_asign[2].recipe.name)


if __name__ == '__main__':
    user = UserProfile('Low-Carb', None, ['tomatoes'], 4000)
    breakfast = Meal(0, 'breakfast')
    lunch = Meal(1, 'lunch')
    dinner = Meal(2, 'dinner')
    current_asign = [breakfast, lunch, dinner]
    constraint_satisfaction(current_asign, user)





# hc = hard constraints, sc = soft constraints
def constraint_satisfaction1(vars_vector, values_vector, hc, sc):
    best_sol = None
    current_assign = []
    lower_bound = 0
    upper_bound = math.inf
    end = False

    var = vars_vector[0]
    val = values_vector[0]
    var.recipe = val
    while not end:
        current_assign.append(var)
        if hc(var):
            lower_bound = sc(var)
            if lower_bound < upper_bound:
                if len(current_assign) == 15:
                    best_sol = current_assign
                    lower_bound = upper_bound
                    new_branch(var)
                else:
                    var = next_var()
                    val = next_val()
            else:
                new_branch(var)
        else:
            new_branch(var)
    return best_sol


'''**********************************'''


def constraint_satisfaction2(vars_vector, values_vector):
    best_sol = None
    current_assign = []
    vars_index = 0
    values_index = 0
    var = vars_vector[vars_index]
    val = values_vector[values_index]
    end = False
    while not end:
        if hc(var, val, current_assign):
            current_assign.append(val)
            if var == 5:
                best_sol = current_assign
                end = True
            else:
                vars_index += 1
                values_index = 0
                var = vars_vector[vars_index]
                val = values_vector[values_index]
        else:
            values_index += 1
            val = values_vector[values_index]
    return best_sol

