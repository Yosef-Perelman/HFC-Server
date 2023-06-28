import logging


def parse_parameters(req):
    logging.info("start parse parameters func")
    result = req.get("queryResult")
    session_id = req.get("session").split('/')[-1]
    parameters = result.get("parameters")


    try:
        age = parameters.get('age')
        logging.info(f"age = {age}")
    except Exception:
        logging.info("error in 'age' parameter")
    try:
        weight = parameters.get('weight')
        logging.info(f"weight = {weight}")
    except Exception:
        logging.info("error in 'weight' parameter")
    try:
        height = parameters.get('height')
        logging.info(f"height = {height}")
    except Exception:
        logging.info("error in 'height' parameter")
    try:
        activity_level = 'level_' + str(parameters.get('activity'))
        logging.info(f"activity_level = {activity_level}")
    except Exception:
        logging.info("error in 'activity_level' parameter")
    try:
        purpose = parameters.get('goal')
        if purpose.isdigit():
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
            logging.info(f"purpose = {purpose_str}")
        else:
            raise Exception
    except Exception:
        logging.info("error in 'purpose' parameter")
    return session_id, age, height, weight, activity_level, purpose_str