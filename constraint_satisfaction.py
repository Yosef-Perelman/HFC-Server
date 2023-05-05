"""
variables = M1,...,M15 - all the meals in the plan
values = all the recipes in the database
hard constraints = all the preliminary requirements of the user
soft constraints = recommended daily intake of calories of the user
"""

import math
import csv


class Recipe:
    def __init__(self, name, type, calories):
        self.name = name
        self.type = type
        self.calories = calories


class Meal:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.recipe = None


def sc(var):
    pass


def new_branch(var):
    pass


def next_var():
    pass


def next_val():
    pass


'''**********************************'''


# hc = hard constraints, sc = soft constraints
def constraint_satisfaction(vars_vector, values_vector, hc, sc):
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


def hc(var, val, current_assign):
    if val in current_assign:
        return False
    if (var % 3) == 0:
        if val.type == 'breakfast':
            return True
    if (var % 3) == 1:
        if val.type == 'lunch':
            return True
    if (var % 3) == 2:
        if val.type == 'dinner':
            return True
    return False


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


if __name__ == '__main__':
    vars = [0, 1, 2, 3, 4, 5]
    values = []

    # opening the CSV file
    with open('db.csv', mode='r') as file:

        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        for lines in csvFile:
            rec = Recipe(lines[0], lines[1], lines[2])
            values.append(rec)

    sol = constraint_satisfaction2(vars, values)
    for meal in sol:
        print(meal.name)
