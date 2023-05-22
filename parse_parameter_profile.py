def parse_parameters1(req):
    result = req.get("queryResult")
    session_id = req.get("session").split('/')[-1]
    output_context = result.get('outputContexts')
    for x in output_context:
        name = x.get("name").split('/')[-1]
        if name == "profile-age-followup":
            context = x
            break
    print(context)
    parameters = context.get("parameters")
    age = parameters.get('age.original')
    print(age)
    weight = parameters.get('weight.original')
    print(weight)
    height = parameters.get('height.original')
    print(height)
    activity_level = 'level_' + str(parameters.get('activity_level.original'))
    print(activity_level)
    purpose = parameters.get('purpose.original')
    print(purpose)
    if purpose == '1':
        purpose_str = 'Maintain weight'
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


def parse_parameters2(req):
    result = req.get("queryResult")
    session_id = req.get("session").split('/')[-1]
    output_context = result.get('outputContexts')
    for x in output_context:
        name = x.get("name").split('/')[-1]
        if name == "forbiddenfoods":
            context = x
            break
    print(context)
    healthLabels = []
    forbiddenfoods = []
    if len(context) == 2:
        parameters = context.get("parameters")
        if len(parameters) == 2:
            if 'Health.original' in parameters:
                healthLabels = parameters.get('Health.original')
            else:
                forbiddenfoods = parameters.get('food_type.original')
        else:
            healthLabels = parameters.get('Health.original')
            forbiddenfoods = parameters.get('food_type.original')
    return session_id, healthLabels, forbiddenfoods