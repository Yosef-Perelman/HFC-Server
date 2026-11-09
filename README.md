# HFC-Server – Nutrition Tracker Backend

Backend of **HFC**, a nutrition-tracking mobile app with a free-language chatbot.
Final project of my B.Sc. in Computer Science at Bar Ilan University (2023), built by a team of two:
I built the whole Python/Flask server, and my partner built the Flutter client.

## What the app does

- **Nutrition diary** – log food in free language and get its nutritional values and daily statistics.
- **Meal planning** – a personalized plan of three meals a day for as many days as the user asks, built by a constraint-satisfaction algorithm.
- **Recipe recommendations** – a content-based recommender that suggests recipes similar to the ones the user liked.
- **Chatbot** – the user talks to the app in free language; Google Dialogflow detects the intent and forwards the request to this server.
- **Daily notifications** – a morning motivation message and an evening reminder to fill in the diary, sent with Firebase Cloud Messaging.

## Architecture

```
Flutter app ──► Dialogflow (intent detection) ──► POST /webhook (Flask)
                                                     │
                                  routes by intent ──┼──► meal_planer.py     (meal.planning)
                                                     ├──► recipe_order.py    (recipe.request)
                                                     ├──► nutrient_info.py   (food.get.info)
                                                     └──► personal_details.py (personal_details)
                                                     │
                     Firebase (Firestore + Storage + FCM) ◄──┤
                     Edamam Recipe & Nutrition APIs ◄────────┤
                     RapidAPI Fitness Calculator ◄───────────┘
```

- `server.py` – Flask app, the Dialogflow webhook, intent routing, and an APScheduler job for the daily notifications.
- Because requests arrive from Dialogflow and not directly from the app, users are identified by a **session ID** stored in the database and checked on every message.

## The algorithms

### Meal planning – Constraint Satisfaction + DFS (`meal_planer.py`)

Each day is a set of three variables (breakfast, lunch, dinner) whose values come from a recipe database (`DB/filtered with images/*.csv`).

- **Hard constraints** – the user's diet type, foods the user must avoid, the recommended daily calorie limit, and recipes the user previously disliked.
- **Soft constraints** – variety of ingredients across the day's meals, and how close the day's total calories are to the user's daily target. Together they give each full assignment a score.

The search walks the tree depth-first: it assigns breakfast, checks the hard constraints, moves on to lunch and then dinner, and backtracks on dead ends. A full assignment is scored by the soft constraints and kept if it beats the threshold and the best solution so far.

**Performance fix:** the first version picked each meal independently, which caused cascading failures and made the search too slow. The fix was to choose each meal within a range of the daily calorie budget and to prune recipes that violate the hard constraints before the next round – after that, a multi-day plan is generated in a few seconds.

### Recipe recommendation – Content-Based Filtering (`recipe_order.py`)

1. Query the Edamam Recipe API with the user's meal type, diet and health labels.
2. Build a feature vector for each returned recipe (ingredients, diet labels, health labels) and a user vector from the recipes the user liked.
3. Rank recipes by **cosine similarity** (NumPy) and pick one of the top three with weighted randomness (50% / 30% / 20%), so recommendations stay varied.

## Tech stack

Python · Flask · Pandas · NumPy · Firebase (Firestore, Storage, Cloud Messaging) · Google Dialogflow · Edamam APIs · RapidAPI · APScheduler · pytest

## Tests

Unit tests for the core logic are written with **pytest** (`test_meal_planner.py`, `test_recipe_order.py`, `test_nutrient_info.py`, `test_parse_parameters.py`, `test_personal_details.py`).

```bash
pytest
```

## Configuration

API keys and credentials are read from environment variables (see `config.py`).
Copy `.env.example` to `.env` and fill in the values. The Firebase service-account JSON file
is not committed; set `FIREBASE_CREDENTIALS` to its path (defaults to the original file name in the project root).

## Running

```bash
pip install flask flask-apscheduler firebase-admin pandas numpy requests python-dotenv
python server.py
```

The webhook URL (`/webhook`) is set as the fulfillment URL in the Dialogflow agent; during development it was exposed with ngrok.
