import json

from django.db import transaction

from nutritionist.models import Product


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = file.read()
        data_dict = json.loads(json_data)
        return data_dict


def from_json_in_db(file_path):
    """
    Получает json с продуктами и записыват из в базу данных.
    Сайчас делаю для Product
    """
    # прочать json файл
    read_json_file(file_path)


@transaction.atomic
def save_products_in_db(menu_items):
    to_create = []
    for product in menu_items:
        to_create.append(Product(
            name=product['name'],
            product_id=product['id'],
            public_name=product['name'],
            carbohydrate=product['carbohydratesAmount'],
            fat=product['fatAmount'],
            fiber=product['proteinsAmount'],
            energy=product['energyAmount'],
            weight=product['weight'],
            description=product['description'],
            category='Десерты',
        ))
    Product.objects.bulk_create(to_create)

def main():
    file_path = "all_product_for_api_1.json"
    # читаем json и записываем в dict
    json_dict = read_json_file(file_path)
    # сохраняем в базе данных
    save_products_in_db(json_dict['products'])


# if __name__ == "__main__":
#    main()