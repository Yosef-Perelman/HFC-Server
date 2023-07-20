import json
from unittest import mock
from nutrient_info import food_get_info


def mock_requests_request(method, url, headers):
    mock_response = mock.Mock()
    mock_response.text = json.dumps({
        "ingredients": [{"text": "Cucumber"}],
        "totalNutrients": {
            "ENERC_KCAL": {"quantity": 10},
            "PROCNT": {"quantity": 1},
            "FAT": {"quantity": 0},
            "CHOCDF": {"quantity": 2},
        }
    })
    return mock_response


def test_food_get_info():
    req = {
        "responseId": "c666fb07-b49e-460f-b34c-503f025667a3-1b0ea404",
        "queryResult": {
            "queryText": "1 cucumber",
            "parameters": {"food_type": "cucumber", "quantity": 1.0, "nutriens": "", "Unit": ""},
        },
    }

    with mock.patch("requests.request", side_effect=mock_requests_request):
        result = food_get_info(req)

    expected_result = (
        "name: Cucumber\n\n"
        "calories: 10\n"
        "protein: 1\n"
        "fat: 0\n"
        "carbohydrates: 2"
    )
    assert result == expected_result


def test_food_get_info_with_quantity_and_unit():
    req = {
        "responseId": "c666fb07-b49e-460f-b34c-503f025667a3-1b0ea404",
        "queryResult": {
            "queryText": "2 tomatoes grams",
            "parameters": {"food_type": "tomatoes", "quantity": 2.0, "nutriens": "", "Unit": "grams"},
        },
    }

    with mock.patch("requests.request", side_effect=mock_requests_request):
        result = food_get_info(req)

    expected_result = (
        "name: Cucumber\n\n"
        "calories: 10\n"
        "protein: 1\n"
        "fat: 0\n"
        "carbohydrates: 2"
    )
    assert result == expected_result


def test_food_get_info_with_missing_quantity_and_unit():
    req = {
        "responseId": "c666fb07-b49e-460f-b34c-503f025667a3-1b0ea404",
        "queryResult": {
            "queryText": "apple",
            "parameters": {"food_type": "apple", "quantity": None, "nutriens": "", "Unit": ""},
        },
    }

    with mock.patch("requests.request", side_effect=mock_requests_request):
        result = food_get_info(req)

    expected_result = (
        "name: Cucumber\n\n"
        "calories: 10\n"
        "protein: 1\n"
        "fat: 0\n"
        "carbohydrates: 2"
    )
    assert result == expected_result


