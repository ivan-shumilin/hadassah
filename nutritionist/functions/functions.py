import re

from doctor.functions.download import get_name_by_api, get_measure_unit
from nutritionist.models import ProductStorage, CustomUser, Product, MenuByDay, Ingredient, TTK
from django.db.models import Q
from datetime import datetime, date, timedelta
from doctor.functions.bot import formatting_full_name

def create_products_list_category(category, meal):
    """ Создет список словарей с продуктами и их колличеством. """

    products_all = []
    products_list = ProductStorage.objects \
        .filter(meal=meal, date_create=date.today(), category=category)
    for product in products_list:
        for product_dly_sravneniya in products_all:
            if product.products_id.split('-')[2] == product_dly_sravneniya['id']:
                product_dly_sravneniya['count'] += 1
                product_dly_sravneniya['type_of_diet'].add(product.type_of_diet)
                break
        else:
            products_all.append({
                'category': category,
                'id': product.products_id.split('-')[2],
                'name': Product.objects.get(id=product.products_id.split('-')[2]).public_name,
                'type_of_diet': {product.type_of_diet},
                'count': 1,
            })
    return products_all


def complete_catalog(category_dict):
    number = 0  # порядковый номер блюд
    for products in category_dict.values():
        for product in products:
            number += 1
            product['number'] = number
            product['type_of_diet_for_print'] = ', '.join(product['type_of_diet'])
    return category_dict


def checking_is_ready_meal(meal):
    time_ready_meals = {
        'breakfast': 9,
        'lunch': 12,
        'dinner': 17
    }
    # время до которого кормим пациентов
    time_finish = {
        'breakfast': '11:00',
        'lunch': '14:00',
        'dinner': '21:00'
    }
    if datetime.today().hour >= 19:
        is_ready_meal = False
        patients = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lte=date.today()) | Q(receipt_date=date.today() + timedelta(days=1))
                    & Q(receipt_time__lte=time_finish[meal]))

    elif datetime.today().hour < time_ready_meals[meal]:
        is_ready_meal = False
        patients = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lt=date.today()) | Q(receipt_date=date.today())
                    & Q(receipt_time__lte=time_finish[meal]))
    else:
        is_ready_meal = True
        patients = None
    return is_ready_meal, patients


def create_category_dict(meal, is_ready_meal, patients):
    category_dict = {'porridge': [], 'salad': [], 'soup': [], 'main': [], 'garnish': []}
    if datetime.today().hour >= 19:
        date = datetime.today().date() + timedelta(days=1)
    else:
        date = datetime.today().date()
    if is_ready_meal:
        category_dict = {
            'porridge': create_products_list_category('porridge', meal),
            'salad': create_products_list_category('salad', meal),
            'soup': create_products_list_category('soup', meal),
            'main': create_products_list_category('main', meal),
            'garnish': create_products_list_category('garnish', meal),
        }


    # Прием пищи не сформирован
    else:
        for patient in patients:
            for category, products_list in category_dict.items():
                try:
                    product_id = MenuByDay.objects \
                        .filter(user_id=patient, date=date, meal=meal).values()[0].get(category)
                except:
                    continue
                if product_id is not None:
                    if 'cafe' in product_id:
                        product_set_all = product_id.split(',')
                        for product_id in product_set_all:
                            if 'cafe' in product_id:
                                product_id = re.findall(r'\d+', product_id)[0]
                                for product in products_list:
                                    if product['id'] == product_id:
                                        product['count'] += 1
                                        product['type_of_diet'].add(patient.type_of_diet)
                                        break
                                else:
                                    products_list.append(
                                        {'category': category,
                                         'id': product_id,
                                         'name': Product.objects.get(id=product_id).name,
                                         'type_of_diet': {patient.type_of_diet},
                                         'count': 1})
    return category_dict


def create_stickers_pdf(catalog):
    from fpdf import FPDF
    def create_res_list(product, max_count_in_line, type):
        st_ch1 = '- ' if type == 'products' else '  '
        st_ch2 = '-' if type == 'products' else ' '
        product_list = product.split(' ')
        res = ""
        res_list = []
        for item in product_list:
            if len(res + item) < max_count_in_line:
                res = res + ' ' + item if res != "" else st_ch1 + item
            else:
                res_list.append(res) if res[0] == st_ch2 else res_list.append('  ' + res)
                res = item
        res_list.append(res) if res[0] == st_ch2 else res_list.append('  ' + res)
        return res_list

    def create_res_list_comment(product, max_count_in_line, type):
        st_ch1 = '- ' if type == 'products' else ''
        st_ch2 = '-' if type == 'products' else ''
        product_list = product.split(' ')
        res = ""
        res_list = []
        for item in product_list:
            if len(res + item) < max_count_in_line:
                res = res + ' ' + item if res != "" else st_ch1 + item
            else:
                res_list.append(res) if res[0] == st_ch2 else res_list.append('' + res)
                res = item
        res_list.append(res) if res[0] == st_ch2 else res_list.append('' + res)
        return res_list

    # рассчет, сколько строк нужно будет скипнуть, чтобы напечатать в конце страницы + печать времени
    def print_date(cell_height):
        height = pdf.h
        current_y = pdf.get_y()
        skip_height = int(height - current_y - cell_height - 10 * 2) # оставляю еще строчку снизу
        pdf.ln(skip_height)
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        pdf.cell(200, cell_height, txt="Время приготовления: " + current_time, ln=True, align="R")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10) # установила фиксированный оступ снизу 10
    for floor in ['users_not_floor', 'users_2nd_floor', 'users_3nd_floor', 'users_4nd_floor']:
        for item in catalog[floor]:
            item['diet'] = item['diet'].replace('*', '')
            pdf.set_left_margin(3)
            pdf.set_right_margin(0)
            pdf.add_page()
            pdf.add_font("Arial1", "", "FontsFree-Net-arial-bold.ttf", uni=True)
            pdf.set_font("Arial1", style='', size=50)
            ln = 1
            if floor == 'users_2nd_floor':
                print_floor = '2 этаж'
            elif floor == 'users_3nd_floor':
                print_floor = '3 этаж'
            elif floor == 'users_4nd_floor':
                print_floor = '4 этаж'
            else:
                print_floor = ''
            department = item['department'] if item["department"] != "Не выбрано" else ""
            department = 'Терапия' if department == 'Онкология' else department
            room_number = f'{item["room_number"] if item["room_number"] != "Не выбрано" else ""}{"" if item["bed"] == "Не выбрано" or item["room_number"] == "Не выбрано" else ", " + item["bed"]}'
            if room_number:
                print_floor = room_number
            if department and print_floor:
                head_top = print_floor + ", " + department
            else:
                head_top = print_floor + department
            if head_top:
                pdf.cell(50, 14, txt=f'{head_top}', ln=ln, align="L")
                ln += 1
            pdf.add_font("Arial1", "", "FontsFree-Net-arial-bold.ttf", uni=True)
            pdf.set_font("Arial1", style='', size=33)
            head = f'{formatting_full_name(item["name"])}'
            head = head.strip()
            pdf.cell(50, 14, txt=f'{head}', ln=ln, align="L")

            ln += 1
            if item["diet"] == "ОВД веган (пост) без глютена":
                pdf.cell(50, 14, txt=f'ОВД веган (пост) без глютена,', ln=ln, align="L")
                ln += 1
                pdf.cell(50, 14, txt=f'{catalog["meal"].lower()}, {date.today().day}/{date.today().month}/{str(date.today().year)[2:]}', ln=ln, align="L")
                ln += 1
            else:
                pdf.cell(50, 14, txt=f'{item["diet"]}, {catalog["meal"].lower()}, {date.today().day}/{date.today().month}/{str(date.today().year)[2:]}', ln=3, align="L")
                ln += 1
            pdf.add_font("Arial2", "", "arial.ttf", uni=True)
            pdf.set_font("Arial2", style='', size=30)

            max_count_in_line = 38
            if item["comment"]:
                item["comment"] = item["comment"].capitalize()
                pdf.set_left_margin(3)
                pdf.underline = True
                if len(item["comment"]) >= max_count_in_line:
                    res_list = create_res_list_comment(item["comment"], max_count_in_line, 'comment')
                    for product in res_list:
                        pdf.cell(50, 10, txt=f'{product}', ln=ln, align="L")
                        ln += 1
                else:
                    pdf.cell(50, 10, txt=f'{item["comment"]}', ln=ln, align="L")
                pdf.underline = False

            ln += 1
            pdf.cell(50, 10, txt="", ln=5, align="L")
            ln += 1

            for index, product in enumerate(item['products_lp']):

                if len(product['name']) >= max_count_in_line:
                    res_list = create_res_list(product['name'], max_count_in_line, 'products')
                    for product in res_list:
                        pdf.cell(50, 10, txt=f'{product}', ln=index + ln, align="L")
                        ln += 1
                else:
                    pdf.cell(50, 10, txt=f'- {product["name"]}', ln=index + ln, align="L")
                pdf.cell(50, 3, txt=f'', ln=index + 1 + ln, align="L")

            # проверка, что время вместиться на страницу, иначе не печатаю
            # 10 - отступ снизу, 10 - высота клетки
            if pdf.h - pdf.get_y() >= (10 + 10):
                print_date(10)

    pdf.output("static/stickers.pdf")
    return

def add_try(report):
    """ Добавляем суточные пробы. """
    exception = ['Вода "Jеvea" 0,51л.',
                    'Булочка французская 35гр. в асс.',
                    'Булочка французская 35гр. в асс, 2 шт',
                    'Булочка французская 35гр. в асс., 3 шт',
                    'Хлеб бородинский/ржаной 20 гр., 2 шт.',
                    'Хлеб из зеленой гречки пряный 35 гр., 2 шт.',
                    'Батончик  "SOJ" в асс.',
                    'R.A.W. криспы кокос-манго 35 гр',
                    'Nutrien Sugarless 200 мл',
                    'Nutrien Standard 200 мл',
                 ]
    for product in report:
        if product['name'] not in exception:
            product['count'] += 1


def cleaning_null(catalog):
    catalog_ = {}
    for key1, meal in catalog.items():
        catalog_[key1] = {}
        for key2, category in meal.items():
            if len(category) > 0:
                catalog_[key1][key2] = category
    return catalog_


def combine_broths(soups):
    """ Объединяет "Бульон" и "Дополнительный бульон". """
    broth_product_id = 'b95797d9-7b21-46dd-9f61-87157e2eec66'
    finish = len(soups)
    for start in range(finish):
        if soups[start] and soups[start]['product_id'] == broth_product_id:
            soups[start]['name'] = 'Бульон куриный 250гр.'
            for i in range(start + 1, finish):
                if soups[i]['product_id'] == broth_product_id:
                    deleted_product = soups[i]
                    soups[i] = None
                    soups[start]['count'] = \
                        int(soups[start]['count']) + int(deleted_product['count'])
                    soups[start]['comments'] += deleted_product['comments']
                    soups[start]['diet'] += deleted_product['diet']
    return soups


def get_coefficient(weight_pf_main: float, weight_pf_local: float, count: int) -> int:
    """
    Расчет коофицента для получения веса ингредиента.
    """
    if 0 in (weight_pf_main, weight_pf_local, count):
        return 0
    else:
        return weight_pf_main / weight_pf_local * count


def get_name_and_measure_unit(product_id: str) -> (str, str):
    """
    Получение имени ингредиенты и единицу измнения
    """
    ingredient = Ingredient.objects.filter(product_id=product_id).first()
    try:
        return ingredient.name, ingredient.measureUnit
    except:
        return get_name_by_api(product_id), get_measure_unit(product_id)


def create_ttk(ttk: dict, name_product_id: str, parent_ttk=None):
    """
    Записываем ТТК в базу.
    """
    ingredient = Ingredient.objects.filter(product_id=ttk[name_product_id]).first()
    ttk = TTK.objects.create(
        product_id=ttk[name_product_id],
        name=ttk.get('name', None),
        amount_in=ttk.get('amountIn', None),
        amount_middle=ttk.get('amountMiddle', None),
        amount_out=ttk.get('amountOut', None),
        measure_unit=ttk.get('measure_unit', None),
        parent_ttk=parent_ttk,
        ingredient=ingredient,
    )

    return ttk