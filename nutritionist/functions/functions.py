from nutritionist.models import ProductStorage, CustomUser, Product, MenuByDay
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
            if product.products_id == product_dly_sravneniya['id']:
                product_dly_sravneniya['count'] += 1
                product_dly_sravneniya['type_of_diet'].add(product.type_of_diet)
                break
        else:
            products_all.append(
                {'category': category,
                    'id': product.products_id,
                    'name': Product.objects.get(id=product.products_id.split('-')[2]).public_name,
                    'type_of_diet': {product.type_of_diet},
                    'count': 1})
    return products_all


def complete_catalog(category_dict):
    number = 0  # порядковый номер блюд
    for products in category_dict.values():
        for product in products:
            number += 1
            product['number'] = number
            product['type_of_diet'] = ', '.join(product['type_of_diet'])
    return category_dict

def checking_is_ready_meal(meal):
    time_ready_meals = {
        'lunch': 11,
        'dinner': 17
    }
    if datetime.today().hour < time_ready_meals[meal]:
        patients = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lt=date.today()) | Q(receipt_date=date.today()) & Q(receipt_time__lte='14:00'))
        is_ready_meal = False
    else:
        is_ready_meal = True
        patients = None
    return is_ready_meal, patients


def create_category_dict(meal, is_ready_meal, patients):
    category_dict = {'salad': [], 'soup': [], 'main': [], 'garnish': []}
    if is_ready_meal:
        category_dict = {
            'salad': create_products_list_category('salad', meal),
            'soup': create_products_list_category('soup', meal),
            'main': create_products_list_category('main', meal),
            'garnish': create_products_list_category('garnish', meal)}

    # Прием пищи не сформирован
    else:
        for patient in patients:
            for category, products_list in category_dict.items():
                product_id = MenuByDay.objects \
                    .filter(user_id=patient, date=date.today(), meal=meal).values()[0].get(category)
                if product_id is not None:
                    if 'cafe' in product_id:
                        for product in products_list:
                            if product['id'] == product_id.split('-')[2]:
                                product['count'] += 1
                                product['type_of_diet'].add(patient.type_of_diet)
                                break
                        else:
                            product_id = product_id.split('-')[2]
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

    pdf = FPDF()
    for floor in ['users_2nd_floor', 'users_3nd_floor', 'users_4nd_floor', 'users_not_floor']:
        for item in catalog[floor]:
            pdf.set_left_margin(3)
            pdf.set_right_margin(0)
            pdf.add_page()
            pdf.add_font("Arial1", "", "FontsFree-Net-arial-bold.ttf", uni=True)
            pdf.set_font("Arial1", style='', size=33)
            ln = 1
            head = f'{formatting_full_name(item["name"])} {", " + item["room_number"] if item["room_number"] != "Не выбрано" else ""} {"" if item["bed"] == "Не выбрано" or item["room_number"] == "Не выбрано" else ", " + item["bed"]}'
            head = head.strip()
            if len(f'{head}, {item["department"]}') < 30:
                pdf.cell(50, 14, txt=f'{head}, {item["department"]}', ln=ln, align="L")
            else:
                pdf.cell(50, 14, txt=head, ln=ln, align="L")
                ln += 1
                pdf.cell(50, 14, txt=item["department"], ln=ln, align="L")
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

            for index, product in enumerate(item['products_lp'] + item['products_cafe']):
                if len(product) >= max_count_in_line:
                    res_list = create_res_list(product, max_count_in_line, 'products')
                    for product in res_list:
                        pdf.cell(50, 10, txt=f'{product}', ln=index + ln, align="L")
                        ln += 1
                else:
                    pdf.cell(50, 10, txt=f'- {product}', ln=index + ln, align="L")
                pdf.cell(50, 3, txt=f'', ln=index + 1 + ln, align="L")
    pdf.output("static/stickers.pdf")
    return