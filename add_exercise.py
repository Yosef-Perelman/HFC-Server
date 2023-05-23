import json

import requests

swimming = 'wimming laps, freestyle, slow'
football = 'laying soccer'
basketball = 'asketball game, competitive'
running = 'unning, 7.5mph'
walking = 'ace walking'
cycling = 'ycling, 12-13.9 mph'
gym = 'Health club exercise'


def add_exercise_record(req):
	result = req.get("queryResult")
	parameters = result.get("parameters")

	url = "https://calories-burned-by-api-ninjas.p.rapidapi.com/v1/caloriesburned"
	activity = parameters.get('Exercise')
	if activity == 'walking':
		activity = walking
	if activity == 'run':
		activity = running
	if activity == 'cycling':
		activity = cycling
	if activity == 'swimming':
		activity = swimming
	if activity == 'soccer':
		activity = football
	if activity == 'basketball':
		activity = basketball
	if activity == 'gym':
		activity = gym
	duration = parameters.get('duration')
	# should get the user weight
	querystring = {"activity": activity, "weight": "75", "duration": duration}

	headers = {
		"X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
		"X-RapidAPI-Host": "calories-burned-by-api-ninjas.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response.text)

	response_dict = json.loads(response.text)
	return "burned calories: " + str(response_dict[0]['total_calories'])