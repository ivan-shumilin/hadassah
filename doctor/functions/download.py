# получаем по api список всех тех. карт и сохраняем в базу в json
import datetime
import json

import requests

from nutritionist.models import ProductLp, Ingredient


def get_token():
    url = 'https://petrushka-grupp-skolkovo.iiko.it:443/resto/api/auth'

    params = {
        'login': 'Admin',
        'pass': '601f1889667efaebb33b8c12572835da3f027f78',
    }

    respons = requests.get(url=url, params=params)
    if respons.status_code == 200:
        return respons.text
    return 'Error'


def download():
    """ Присвоить всем ProductLp id для обращения за тех. картой по api. """
    bank = []
    all_products = ProductLp.objects.filter(status=1)
    count = 0

    for product in all_products:
        try:
            product.product_id = Ingredient.objects.get(name=product.name).product_id
            product.save()
            count += 1
        except:
            try:
                product.product_id = Ingredient.objects.get(code=product.number_tk).product_id
                product.save()
                count += 1
            except:
                bank.append(product.name)
    return print(f'Всего: {all_products.count()} -- получено: {count}')


def get_tk(token, product_id):
    """ Получение ТК по iiko api """
    url = 'https://petrushka-grupp-skolkovo.iiko.it:443/resto/api/v2/assemblyCharts/getTree'

    headers = {
        'Cookie': f'key={token}'
    }
    params = {'date': str(datetime.date.today()),
              'productId': product_id,}

    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code != 200:
        return '', 'Server error'
    else:
        tk = json.loads(response.text)
    return tk, ''

def get_name(token, product_id):
    """ Получаем элемент номенклатуры. """
    url = 'https://petrushka-grupp-skolkovo.iiko.it:443/resto/api/v2/entities/products/list?includeDeleted=false'

    headers = {
        'Cookie': f'key={token}'
    }
    params = {'ids': product_id}


    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code != 200:
        return '', 'Server error'
    else:
        tk = json.loads(response.text)
        try:
            name = tk[0]['name']
        except:
            name = None
    return name
