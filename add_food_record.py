'''def rapid_api_nutrition_info():

    url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"

    querystring = {"ingr": "bread"}

    headers = {
        "X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
        "X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    response_dict = json.loads(response.text)
    name = response_dict["parsed"][0]["food"]["nutrients"]
    print(name)


def test_firebase():
    food_name = "Tomato"
    results = collection.find({"Food": food_name})
    for result in results:
        print(result)
        calories = result["Calories"]
    doc_ref = usersDB.collection(u'users').document(u'yosef').collection(date).collection(u'breakfast').document(u'intent_id')
    # .collection(datetime.now().strftime("%m/%d/%Y")).document(parameters.get("Meal"))
    doc_ref.set({
        u'name': food_name,
        u'calories': calories
    })


def add_food_record():
    meal = parameters.get("Meal")
    calories = 0
    for food in parameters.get("Food_Type"):
        print("food: ", food)
        food_name = capitalize_words(food)
        results = collection.find({"Food": food_name})
        for result in results:
            print(result)
            calories = result["Calories"]
        # doc_ref = usersDB.collection(u'users').document(u'eli')
        doc_ref = usersDB.collection(u'users').document(u'yosef').collection(date).document(meal). \
            collection(sessionID).document(food_name)
        # .collection(datetime.now().strftime("%m/%d/%Y")).document(parameters.get("Meal"))
        doc_ref.set({
            u'name': food_name,
            u'calories': calories
        })

    return 'the record added!'''''