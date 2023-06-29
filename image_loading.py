import json
import pandas as pd
import requests
from firebase_admin import storage
import logging


def download_image(url, name):
    logging.info("start download image func")
    bucket = storage.bucket()
    blob = bucket.blob(f'recipes_images/{name}.jpg')
    if not blob.exists():
        logging.info("the image didn't exist in the storage, trying to download it from the web...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open("image.jpg", 'wb') as file:
                    file.write(response.content)
                blob.upload_from_filename("image.jpg")
                blob.make_public()
                logging.info("Image downloaded successfully!")
                return blob.public_url
            else:
                logging.info("Failed to download image.")
                # todo: handle in the case of error in downloading image
                return None
        except Exception:
            logging.error("error in getting the recipe image")
    else:
        return blob.public_url


def download_image_by_name(name):
    pass


def images_arrange():
    df = pd.read_csv('DB/filtered/filtered_breakfast.csv')

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    picture = ""

    for index, row in df.iterrows():
        name = row['name']
        format_name = name.replace(' ', '%20')
        link = f"https://api.edamam.com/api/recipes/v2?type=public&q={format_name}&app_id=3749f87d&app_key=191597bb0eccc02907ba8e5efb98fc8b"

        response = requests.request("GET", link, headers=headers)
        response_dict = json.loads(response.text)

        for recipe in response_dict['hits']:
            if recipe['recipe']['label'] == name:
                try:
                    picture = recipe['recipe']['images']['LARGE']['url']
                except:
                    picture = recipe['recipe']['images']['REGULAR']['url']
                break

        response = requests.get(picture)
        if response.status_code == 200:
            with open("image.jpg", 'wb') as file:
                file.write(response.content)
            bucket = storage.bucket()
            blob = bucket.blob(f'recipes_images/{name}.jpg')
            blob.upload_from_filename("image.jpg")
            blob.make_public()
            print("your file url", blob.public_url)
            print("Image downloaded successfully!")
            return blob.public_url
        else:
            print("Failed to download image.")


def images_arrange_for_one_pic():

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en"
    }

    picture = ""

    name = 'brioche french toast casserole'
    bucket = storage.bucket()
    blob = bucket.blob(f'recipes_images/{name}.jpg')

    if not blob.exists():
        format_name = name.replace(' ', '%20')
        link = f"https://api.edamam.com/api/recipes/v2?type=public&q={format_name}&app_id=3749f87d&app_key=191597bb0eccc02907ba8e5efb98fc8b"

        response = requests.request("GET", link, headers=headers)
        response_dict = json.loads(response.text)

        for recipe in response_dict['hits']:
            lower = recipe['recipe']['label'].lower()
            if  lower == name:
                try:
                    picture = recipe['recipe']['images']['LARGE']['url']
                except:
                    picture = recipe['recipe']['images']['REGULAR']['url']
                break

        response = requests.get(picture)
        if response.status_code == 200:
            with open("image.jpg", 'wb') as file:
                file.write(response.content)
            blob.upload_from_filename("image.jpg")
            blob.make_public()
            print("your file url", blob.public_url)
            print("Image downloaded successfully!")
            return blob.public_url
        else:
            print("Failed to download image.")
    else:
        print(f"File '{f'recipes_images/{name}.jpg'}' already exists in Firebase Storage.")

