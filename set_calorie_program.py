import json

import requests


def set_calorie_daily(req):
	result = req.get("queryResult")
	output_context = result.get('outputContexts')
	context = output_context[2]
	parameters = context.get("parameters")
	age = parameters.get('age.original')
	gender = parameters.get('Gender.original')
	weight = parameters.get('weight.original')
	height = parameters.get('height.original')
	activity_level = 'level_3'

	url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

	querystring = {"age":age,"gender":gender,"height":height,"weight":weight,"activitylevel":activity_level}

	headers = {
		"X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
		"X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response.text)
	response_dict = json.loads(response.text)
	print("your daily calories: " + str(response_dict['data']['goals']['Weight loss']['calory']))
	return "your daily calories: " + str(int(response_dict['data']['goals']['Weight loss']['calory']))