# Получаем по iiko api cloud список всех nomenclature
# nomenclature  --> Ingredient
import json

import requests
from django.db import transaction

from nutritionist.models import ProductLp, Ingredient


def get_token():
    url = 'https://api-ru.iiko.services/api/1/access_token'

    data = {
        "apiLogin": "3eca5c01-145"
    }

    response = requests.post(url=url, json=data)
    token = response.json().get('token')
    # if respons.status_code == '200':
    #     return respons.text
    # return 'Error'
    return token


def get_nomenclature(token: str) -> list:
    url = 'https://api-ru.iiko.services/api/1/nomenclature'

    headers = {'Authorization': f'Bearer {token}'}

    data = {
        "organizationId": "b486b89e-527c-431d-8136-25b7ac840d4b",
        "startRevision": 0
        }

    response = requests.post(url=url, headers=headers, json=data)
    nomenclature = json.loads(response.text)

    return nomenclature


@transaction.atomic
def create_ingredients(by_api=True):
    """ Создает Ingredient. """
    token = get_token()

    if by_api:
        nomenclature = get_nomenclature(token)
    else:
        with open("doctor/nomenclature.json", "r") as my_file:
            nomenclature = json.load(my_file)
    to_create = []
    Ingredient.objects.all().delete()
    for product in nomenclature['products']:
        to_create.append(Ingredient(
            product_id=product["id"],
            name=product["name"],
            imageLinks = product["imageLinks"],
            code = product["code"],
            description = product["description"],
            fatAmount = product["fatAmount"],
            proteinsAmount = product["proteinsAmount"],
            carbohydratesAmount = product["carbohydratesAmount"],
            energyAmount = product["energyAmount"],
            fatFullAmount = product["fatFullAmount"],
            proteinsFullAmount = product["proteinsFullAmount"],
            carbohydratesFullAmount = product["carbohydratesFullAmount"],
            energyFullAmount = product["energyFullAmount"],
            weight = product["weight"],
            groupId = product["groupId"],
            productCategoryId = product["productCategoryId"],
            type = product["type"],
            orderItemType = product["orderItemType"],
            measureUnit = product["measureUnit"],
        ))
    Ingredient.objects.bulk_create(to_create)

