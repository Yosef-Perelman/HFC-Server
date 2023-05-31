
def parse_parameters2(req):
    result = req.get("queryResult")
    session_id = req.get("session").split('/')[-1]
    parameters = result.get("parameters")
    age = parameters.get('age')
    print(age)
    weight = parameters.get('weight')
    print(weight)
    height = parameters.get('height')
    print(height)
    activity_level = 'level_' + str(parameters.get('activity'))
    print(activity_level)
    purpose = parameters.get('goal')
    print(purpose)
    if purpose == '1':
        purpose_str = 'maintain weight'
    elif purpose == '2':
        purpose_str = "Mild weight loss"
    elif purpose == '3':
        purpose_str = "Weight loss"
    elif purpose == '4':
        purpose_str = "Extreme weight loss"
    elif purpose == '5':
        purpose_str = "Mild weight gain"
    elif purpose == '6':
        purpose_str = "Weight gain"
    else:
        purpose_str = "Extreme weight gain"
    return session_id, age, height, weight, activity_level, purpose_str