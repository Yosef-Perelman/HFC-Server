import recipe_order as ro
import data


def create_params(meal, health, diet, dish):
    meal = meal
    meal_query = ""
    if meal:
        print(meal)
        meal_query = "&mealType=" + meal
    health = health
    health_query = ""
    if health:
        print(health)
        health_query = "&health=" + health
    diet = diet
    diet_query = ""
    if diet:
        diet = ro.format_string(diet)
        print(diet)
        diet_query = "&diet=" + diet
    dish = dish
    dish_query = ""
    if dish:
        dish.replace(' ', '%20')
        print(dish)
        dish_query = "&dishType=" + dish

    return meal_query, health_query, diet_query, dish_query


def test_api():
    '''for tag in data.health_tags:
        format_tag = 'DASH'
        if tag != 'DASH':
            format_tag = ro.format_string(tag)
        if format_tag == 'mediterranean':
            format_tag = 'Mediterranean'

        meal_query, health_query, diet_query, dish_query = create_params(None, format_tag, None, None)
        response = ro.api_request(meal_query, health_query, diet_query, dish_query)
        names = []
        for hit in hits:
            names.append(hit['recipe']['label'])
        print(f"label = {format_tag}.\nresponse = {names}")'''

    '''for tag in data.diet_tags:
        meal_query, health_query, diet_query, dish_query = create_params(None, None, tag, None)
        response = ro.api_request(meal_query, health_query, diet_query, dish_query)
        names = []
        for hit in hits:
            names.append(hit['recipe']['label'])
        print(f"label = {tag}.\nresponse = {names}")'''

    '''for tag in data.meals:
        meal_query, health_query, diet_query, dish_query = create_params(tag, None, None, None)
        response = ro.api_request(meal_query, health_query, diet_query, dish_query)
        names = []
        for hit in hits:
            names.append(hit['recipe']['label'])
        print(f"label = {tag}.\nresponse = {names}")'''

    '''for tag in data.dish_types:
        tag.replace(' ', '%20')
        meal_query, health_query, diet_query, dish_query = create_params(None, None, None, tag)
        response = ro.api_request(meal_query, health_query, diet_query, dish_query)
        hits = response['hits']
        names = []
        for hit in hits:
            names.append(hit['recipe']['label'])
        print(f"label = {tag}.\nresponse = {names}")'''


if __name__ == '__main__':
    test_api()