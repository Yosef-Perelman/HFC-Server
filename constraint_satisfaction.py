"""
variables = M1,...,M15 - all the meals in the plan
values = all the recipes in the database
hard constraints = all the preliminary requirements of the user
soft constraints = recommended daily intake of calories of the user
"""
import ast
import csv
import time


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


def hc(user_profile, meal, recipe, already_chosen):

    if recipe.name in already_chosen:
        return False

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


    # todo: add the constraint that the recipe didn't chosen yet

    if meal.type == 'breakfast':
        if float(recipe.calories) > (user_profile.recommended_calories / 3):
            return False
    if meal.type == 'lunch':
        if float(recipe.calories) > (user_profile.recommended_calories / 2):
            return False
    return True


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


def remove_apostrophe(strings):
    cleaned_strings = []
    for string in strings:
        cleaned_string = string.replace("'", "")
        cleaned_strings.append(cleaned_string)
    return cleaned_strings


def sc(user_profile, recipe, current_assign):
    deviation = abs(float(current_assign[0].recipe.calories) + float(current_assign[1].recipe.calories) +
                    float(recipe.calories) - user_profile.recommended_calories) / 100
    if deviation <= 0.5:
        return 0
    #list1 = remove_apostrophe(current_assign[0].recipe.ingredients)
    #list2 = remove_apostrophe(current_assign[1].recipe.ingredients)
    #list3 = remove_apostrophe(recipe.ingredients)
    unique_ingredients, duplicate_ingredients = count_unique_and_duplicates(current_assign[0].recipe.ingredients,
                                                                            current_assign[1].recipe.ingredients,
                                                                            recipe.ingredients)
    variation = duplicate_ingredients / unique_ingredients / 2
    #variation = 0
    return variation + deviation


'''**********************************'''


def get_csv_row(filename, row_num):
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if i == row_num + 1:
                return row
    return None


def create_recipe(row):
    diet = ast.literal_eval(row[4])
    health = ast.literal_eval(row[5])
    lines = ast.literal_eval(row[6])
    ingredients = ast.literal_eval(row[14])
    return Recipe(row[0], row[1], row[2], row[3], health, diet, lines, row[10], row[11], row[12],
                  row[13], ingredients, row[9], row[7], row[15])


def constraint_satisfaction(user, number_of_days):

    already_chosen = []
    meals = []

    for i in range(number_of_days):
        breakfast = Meal(0, 'breakfast')
        lunch = Meal(1, 'lunch')
        dinner = Meal(2, 'dinner')
        current_asign = [breakfast, lunch, dinner]
        bf = Meal(0, 'breakfast')
        lnch = Meal(1, 'lunch')
        dnnr = Meal(2, 'dinner')
        best_sol = [bf, lnch, dnnr]

        end_of_the_file = 500
        breakfast_index = 1
        lunch_index = 1
        dinner_index = 1
        upper_bound = 100
        end = False
        success = False

        while not end:
            stop_flag = False
            for ass in current_asign:
                if stop_flag:
                    break
                if ass.type == 'breakfast':
                    filename = 'DB/breakfast3.csv'
                    index = breakfast_index
                elif ass.type == 'lunch':
                    filename = 'DB/lunch3.csv'
                    index = lunch_index
                else:
                    filename = 'DB/dinner3.csv'
                    index = dinner_index
                file = open(filename, 'r', encoding='utf8')
                csv_reader = csv.reader(file)
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        continue
                    if i == index:
                        recipe = create_recipe(row)

                        if ass.type == 'breakfast':
                            if hc(user,ass,recipe,already_chosen):
                                ass.recipe = recipe
                                index += 1
                                breakfast_index = index
                                break
                            else:
                                if index < end_of_the_file:
                                    index += 1
                                else:
                                    end = True
                                    stop_flag = True
                                    break

                        elif ass.type == 'lunch':
                            if hc(user, ass, recipe, already_chosen):
                                ass.recipe = recipe
                                index += 1
                                lunch_index = index
                                break
                            else:
                                if index < end_of_the_file:
                                    index += 1
                                else:
                                    breakfast_index += 1
                                    lunch_index = 1
                                    stop_flag = True
                                    break

                        elif ass.type == 'dinner':
                            if hc(user, ass, recipe, already_chosen):
                                lower_bound = sc(user, recipe, current_asign)
                                if lower_bound < upper_bound:
                                    success = True
                                    ass.recipe = recipe
                                    best_sol[0].recipe = current_asign[0].recipe
                                    best_sol[1].recipe = current_asign[1].recipe
                                    best_sol[2].recipe = current_asign[2].recipe
                                    upper_bound = lower_bound
                                    index += 1
                                    if upper_bound <= 1:
                                        end = True
                                        break
                                else:
                                    if index < end_of_the_file:
                                        index += 1
                                    else:
                                        breakfast_index -= 1
                                        lunch_index += 1
                                        break
                            else:
                                if index < end_of_the_file:
                                    index += 1
                                else:
                                    breakfast_index -= 1
                                    lunch_index += 1
                                    break

        for x in best_sol:
            already_chosen.append(x.recipe.name)
            meals.append(x)

        '''else:
            if index < end_of_the_file:
                index += 1
            else:
                if ass.type == 'breakfast':
                    # If the search go over all the breakfasts it means that the search failed and need
                    # to finish
                    print("the search over without good results")
                    end = False
                    stop_flag = True
                    break
                elif ass.type == 'lunch':
                    # If the search go over all the lunches it means that no proper lunch and dinner found and need to
                    # move on to the next breakfast, so break the loop to start from the next breakfast and from the
                    # first lunch
                    breakfast_index += 1
                    lunch_index = 1
                    stop_flag = True
                    break
                else:
                    # If the search go over all the dinners it means that no proper dinner found and need to
                    # move on to the next lunch, so return the breakfast index so it will chose again the same breakfast,
                    # and move the lunch index one step forward to start from the next lunch, and break the loop
                    dinner_index = 1
                    breakfast_index -= 1
                    lunch_index += 1
                    break'''

    day_calories = 0
    for n in range(number_of_days*3):
        if n % 3 == 0:
            if n != 0:
                print("calories of the day = " + str(day_calories))
            print("day number " + str(n / 3 + 1) + ":")
            day_calories = 0
        if meals[n].recipe is not None:
            print(meals[n].type + ":")
            print("name: " + meals[n].recipe.name)
            print("dietLabels: ")
            diet = ""
            for string in meals[n].recipe.dietLabels:
                diet += string + " "
            print(diet)
            print("healthLabels: ")
            health = ""
            for string in meals[n].recipe.healthLabels:
                health += string + " "
            print(health)
            print("ingredients: ")
            ingredients = ""
            for string in meals[n].recipe.ingredients:
                ingredients += string + " "
            print(ingredients)
            print("calories: " + meals[n].recipe.calories)
            day_calories += float(meals[n].recipe.calories)
    print("calories of the day = " + str(day_calories))



if __name__ == '__main__':
    number_of_days = 3
    user = UserProfile(None, 'Vegetarian', ['sugar', 'onion'], 2000)
    start_time = time.time()
    constraint_satisfaction(user, number_of_days)
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds")
