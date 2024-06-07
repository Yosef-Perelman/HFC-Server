# HFC-Server

The starting module is 'server.py'.
It included API routing to the differents webhooks according to the user's choice.
It also included the flask configuration and the ruuning commands.

The main modules of the server, where the magic happens is:
- 'meal_planner.py' for creating a meal plan by an AI algorithm of constraints satisfaction (using Pandas library).
- 'recipe_order.py' for getting recipe recomendation by AI algorithm of personalized Recommended System Content Based Filtering (using NumPy library).

The other modules contain connectivity, support, information, communication, tests and logging.

