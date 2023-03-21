import requests

'''url = "https://calories-burned-by-api-ninjas.p.rapidapi.com/v1/caloriesburned"

querystring = {"activity":"run","weight":"75","duration":"45"}

headers = {
	"X-RapidAPI-Key": "fe8c47f227mshd760ad2995da85bp1a536djsnd48322f3c41e",
	"X-RapidAPI-Host": "calories-burned-by-api-ninjas.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)'''

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