import json, os, requests, random, math, calendar, datetime, re, operator, openpyxl
from dateutil.parser import parse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from django.template import RequestContext
from django.urls import reverse
from django.db import transaction
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import CheckboxInput, Textarea
from django.core.mail import send_mail
from django.db.models.functions import Lower
from django.views.generic import TemplateView

from doctor.functions.download import get_token, get_tk, get_name, get_allergens, get_weight_tk, get_measure_unit
from doctor.tasks import create_report_download
from .functions.report import create_external_report, create_external_report_detailing, get_report
from .models import Base, Product, Timetable, CustomUser, Barcodes, ProductLp, MenuByDay, BotChatId, СhangesUsersToday, \
    UsersToday, UsersReadyOrder, MenuByDayReadyOrder, Report, ProductStorage, IsReportCreate
from .forms import UserRegistrationForm, UserloginForm, TimetableForm, UserPasswordResetForm
from .serializers import ProductSerializer, DownloadReportSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from datetime import datetime, date
from django.core import management
from django.core.management.commands import dumpdata
from django.contrib.auth.models import Group
from doctor.functions.functions import sorting_dishes, parsing, \
    creates_dict_with_menu_patients, creating_meal_menu_lp, creating_meal_menu_cafe, \
    creates_dict_with_menu_patients_on_day, delete_choices, create_user, edit_user, counting_diets, \
    create_list_users_on_floor, what_meal, translate_meal, check_value_two, what_type_order, add_features, \
    get_now_show_meal, translate_first_meal
from doctor.functions.bot import check_change
from doctor.functions.for_print_forms import create_user_today, check_time, update_UsersToday, update_СhangesUsersToday, \
    applies_changes
from doctor.functions.bot import formatting_full_name
from doctor.functions.translator import get_day_of_the_week, translate_diet
import random, calendar, datetime, logging, json
from datetime import datetime, date, timedelta
from django.utils import dateformat
from nutritionist.functions.functions import create_products_list_category, complete_catalog, \
    checking_is_ready_meal, create_category_dict, create_stickers_pdf, add_try, cleaning_null, combine_broths


class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'


def group_nutritionists_check(user):
    return user.groups.filter(name='nutritionists').exists()


def backup(request):
    answer = []
    management.call_command('backup_db_ydisk', stdout=answer)
    return render(request, 'backup.html', {'answer': answer})


@transaction.atomic
def load_menu(dict_tests, dict_tk):
    menu_items = dict_tests['menu']['items']
    to_create = []
    for menu_item in menu_items:
        try:
            if len(menu_item['product']['description']) < 3:
                menu_item['product']['description'] = 'Отсутствует'
        except TypeError:
            menu_item['product']['description'] = 'Отсутствует'
        key = dict_tk.get(menu_item['product']['name'])
        if key == None:
            key = "Отсутствует"

        if (len(Product.objects.filter(iditem=menu_item['product']['id'])) == 0) and (
                len([item for item in to_create if item.iditem == menu_item['product']['id']]) == 0):
            to_create.append(Product(
                iditem=menu_item['product']['id'],
                name=menu_item['product']['name'],
                public_name=menu_item['product']['name'],
                price=menu_item['product']['price'],
                carbohydrate=menu_item['product']['carbohydrate'],
                fat=menu_item['product']['fat'],
                fiber=menu_item['product']['fiber'],
                energy=menu_item['product']['energy'],
                image=menu_item['product']['image'],
                vegan=menu_item['product']['vegan'],
                allergens=menu_item['product']['allergens'],
                lactose_free=menu_item['product']['lactose_free'],
                sugarless=menu_item['product']['sugarless'],
                gluten_free=menu_item['product']['gluten_free'],
                description=menu_item['product']['description'],
                category=menu_item['category']['name'],
                cooking_method=key
            ))
    Product.objects.bulk_create(to_create)


@transaction.atomic
def load_timetable(dict_tests):
    # Product.objects.all().delete()
    # dict_tests = {'menu': {'id': 682, 'date': '24.06.2022', 'status': 'completed', 'completed_at': '22.06.2022 17:52:31', 'created_at': '17.06.2022 10:26:17', 'combo_price': 350, 'location': {'id': 4, 'name': 'hadassah', 'subdomain': 'hadassah'}, 'items': [{'id': 13276, 'combo': False, 'product': {'id': 251, 'name': 'Говядина по-азиатски 75/75 гр.', 'price': 239, 'carbohydrate': '0.57539', 'fat': '11.42332', 'fiber': '21.60205', 'energy': '191.51808', 'image': 'a8faed5c-fd3e-40cf-bb93-6d86240a268e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: говядина, масло подсолнечное, соус соевый, крахмал, соус терияки, перец чили, масло кунжутное, кунжут, корень имбиря, перец болгарский, лук репчатый.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13277, 'combo': False, 'product': {'id': 337, 'name': 'Куриная ватрушка с грибным жульеном 120 гр.', 'price': 159, 'carbohydrate': '23.04720', 'fat': '17.42760', 'fiber': '20.17560', 'energy': '329.73120', 'image': '66366171-300e-469f-8692-de7da76785f4.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : Состав : фарш из курицы ( филе курицы, хлеб, соль, перекц , лук репчатый), масло подсолнечное, сыр Гауда, жульен грибной ( грибы шампиньоны, лук репчатый, масло подсолнечное, молоко 3,2%, сливки 33%, перец черный молотый, соль).'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13278, 'combo': False, 'product': {'id': 396, 'name': 'Перец фаршированный овощами, грибами и кус-кусом 200/50', 'price': 239, 'carbohydrate': '25.70250', 'fat': '8.97750', 'fiber': '4.95250', 'energy': '203.40750', 'image': '7bba3000-acb3-4b5d-aecd-aa0b7be477e5.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: перец болгарский, грибы шампиньоны, кускус, морковь, перец болгарский, томатный соус ( томатная паста, лук репчатый, морковь, перец черный молотый, соль, прованские травы),'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13279, 'combo': True, 'product': {'id': 1817, 'name': 'Суп-крем овощной 250 гр.', 'price': 99, 'carbohydrate': '21.50694', 'fat': '5.40708', 'fiber': '2.86319', 'energy': '146.14958', 'image': 'fb998852-3579-4a9a-bba7-abe5cccb8f32.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста брокколи, капуста цветная , лук репчатый, картофель, морковь, зхелень, сельдерей, перец, соль, масло оливковое, сливки 33 % .'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13280, 'combo': False, 'product': {'id': 1255, 'name': 'Тайский суп с лапшой и говядиной 250 гр.', 'price': 169, 'carbohydrate': '17.91500', 'fat': '14.48250', 'fiber': '15.07500', 'energy': '262.29000', 'image': '76113578-d361-41f9-9bad-31a37e26c856.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: шпинат, говядина, чеснок, имбирь, лук репчатый, морковь, масло подсолнечное, грибы шампиньоны, лапша гречневая, соевый соус, соль, перец.'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13281, 'combo': False, 'product': {'id': 434, 'name': 'Стейк из бедра индейки с томатной сальсой 100/50 гр.', 'price': 239, 'carbohydrate': '3.64950', 'fat': '16.14150', 'fiber': '21.92400', 'energy': '247.57050', 'image': 'df5fb311-1b7f-4373-bc4d-2ca869c8b3e7.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : филе индейки, соевый соус, тимьян, мед, масло подсолнечное, томатная сальса( помидор, лук репчатый, чеснок, кинза, соль, перец, масло оливковое).'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13282, 'combo': True, 'product': {'id': 446, 'name': 'Тефтели куриные с зеленым горошком в сметанном соусе 100/50гр.', 'price': 139, 'carbohydrate': '16.39800', 'fat': '12.20250', 'fiber': '14.38200', 'energy': '232.92450', 'image': '1b066181-48e5-4739-b847-6819afa21f54.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: фарш куриный (курица, соль, перец, лук, хлеб),горек зеленый, сметана, мука пшеничная, соль,перец черный молотый.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13283, 'combo': False, 'product': {'id': 514, 'name': 'Брокколи на пару с болгарским перцем 150 гр.', 'price': 119, 'carbohydrate': '7.41150', 'fat': '5.26650', 'fiber': '3.73650', 'energy': '91.98150', 'image': '0f3a5af0-8454-4441-a5f6-c53655b1b2b3.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста брокколи с/м, перец болгарский, масло подсолнечное'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13284, 'combo': True, 'product': {'id': 617, 'name': 'Спагетти отварные 150 гр.', 'price': 69, 'carbohydrate': '35.74950', 'fat': '7.15650', 'fiber': '4.68000', 'energy': '226.12350', 'image': '66149542-2a5f-426e-9e58-bf327a581b76.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав Спагетти, масло подс.,соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13285, 'combo': False, 'product': {'id': 359, 'name': 'Лазанья грибная 200 гр.', 'price': 199, 'carbohydrate': '56.29400', 'fat': '14.49800', 'fiber': '19.03600', 'energy': '431.79400', 'image': 'f82d609c-7824-4492-b297-a0616726f9cb.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : грибы шампиньоны, лук репчатый, масло подсолнечное, паста для лазаньи, перец черный молотый, соль, сыр гауда, соус бешамель ( масло сливочное, молоко 3,2%, мускатный орех, мука пшеничная, соль, перец черный молотый.)'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13286, 'combo': False, 'product': {'id': 1218, 'name': 'Суп рисовый с куриными фрикадельками 250 гр.', 'price': 89, 'carbohydrate': '10.14000', 'fat': '4.60750', 'fiber': '6.47750', 'energy': '107.94000', 'image': 'dd6bbb7a-d17c-4725-b8b8-2da02e2012db.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав Бульон куриный, фрикадельки из куриного фарша,рис, морковь, лук репчатый,соль , перец'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13287, 'combo': False, 'product': {'id': 508, 'name': ' Картофельное пюре со шпинатом150 гр.', 'price': 89, 'carbohydrate': '26.91450', 'fat': '7.95750', 'fiber': '4.05450', 'energy': '195.50250', 'image': 'ee560f38-5b7b-41f8-8275-a4a2b3e7f8b1.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Картофель,молоко,масло сливочное,шпинат с/м.,соль'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13288, 'combo': False, 'product': {'id': 1642, 'name': 'Рис с укропом150 гр.', 'price': 69, 'carbohydrate': '47.23619', 'fat': '4.42347', 'fiber': '3.91797', 'energy': '241.06339', 'image': 'fb9a613c-3095-4a6b-a194-5a695b628b90.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Cостав:Рис,шпинат,масло раст.,специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13289, 'combo': False, 'product': {'id': 927, 'name': 'Салат "Столичный" с курицей 100 гр.', 'price': 89, 'carbohydrate': '5.98515', 'fat': '9.44750', 'fiber': '6.03912', 'energy': '133.12458', 'image': '298406ab-7fd7-4b54-8c47-ac94ea3ac828.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, морковь, филе куриное, огурцы маринованные, огурцы свежие, горошек консерв, яйцо куриное отварное, майонез, зелень, соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13290, 'combo': False, 'product': {'id': 947, 'name': 'Салат из крабовых палочек 100 гр.', 'price': 89, 'carbohydrate': '5.40000', 'fat': '9.16500', 'fiber': '2.91000', 'energy': '115.72500', 'image': '606430d1-cf3b-4d6d-ac82-050ed6bf6bd0.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Огурцы свежие, капуста пекинская, крабовые палочки,масйонез, кукуруза консервированная.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13291, 'combo': False, 'product': {'id': 992, 'name': 'Салат из томатов с редисом 100 гр.', 'price': 109, 'carbohydrate': '3.58000', 'fat': '5.16000', 'fiber': '0.80500', 'energy': '63.98000', 'image': '1c25edbd-0443-4865-a7e0-ba0c9417e44f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Помидоры свежие, редис, укроп, масло раст., соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13292, 'combo': True, 'product': {'id': 976, 'name': 'Салат из свежей капусты с зеленым горошком 100 гр.', 'price': 79, 'carbohydrate': '4.82248', 'fat': '7.27273', 'fiber': '2.26123', 'energy': '93.78938', 'image': '5f3ea239-a7b2-47e8-9de5-3ca456a6e175.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста белокачанная, горошек консерв., зелень, масло раст., соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13293, 'combo': False, 'product': {'id': 958, 'name': 'Салат из огурцов с укропом 100 гр.', 'price': 89, 'carbohydrate': '2.87000', 'fat': '2.12600', 'fiber': '0.86200', 'energy': '34.06200', 'image': 'cc924895-5a6e-49d3-b344-13173340541a.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Cостав:Огурцы свежие, укроп,масло раст.,соль'}, 'category': {'id': 15, 'name': 'Салаты'}}]}}

    menu_items = dict_tests['menu']['items']
    to_create = []
    for menu_item in menu_items:
        menu_item_date = datetime.strptime(dict_tests['menu']['date'], "%d.%m.%Y").strftime("%Y-%m-%d")
        if len(Timetable.objects.filter(datetime=menu_item_date).filter(
                item=Product.objects.get(iditem=menu_item['product']['id']))) == 0:
            to_create.append(Timetable(
                datetime=menu_item_date,
                item=Product.objects.get(iditem=menu_item['product']['id'])
            ))
    Timetable.objects.bulk_create(to_create)


# загрузка блюд из json в БД после парсинга
@transaction.atomic
def load_product():
    with open("new_products.json", "r") as my_file:
        new_products = my_file.read()
    new_products = json.loads(new_products)
    to_create = []
    for product in new_products:
        to_create.append(Product(
            name=product['name'],
            date_create=date.today(),
            public_name=product['name'],
            carbohydrate=product['carbohydrate'],
            fat=product['fat'],
            fiber=product['fiber'],
            energy=product['energy'],
            description=product['composition'],
            category=product['category'],
        ))
    Product.objects.bulk_create(to_create)


def redirect(request):
    return HttpResponseRedirect(reverse('login'))

def get_modelformset():
    return modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
                                              'vbd', 'nbd', 'nkd', 'ovd_vegan', 'shd_sugarless', 'iodine_free',
                                              'vkd', 'not_suitable', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
                                              'cooking_method', 'comment'),
                                          widgets={'ovd': CheckboxInput(
                                              attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'ovd_sugarless': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'ovd_vegan': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'shd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'shd_sugarless': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'bd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'vbd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'nbd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'nkd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'vkd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'iodine_free': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'not_suitable': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'name': Textarea(attrs={'style': "display: none;"}),
                                              'description': Textarea(attrs={'style': "display: none;"}),
                                              'carbohydrate': Textarea(attrs={'style': "display: none;"}),
                                              'iditem': Textarea(attrs={'style': "display: none;"}),
                                              'fat': Textarea(attrs={'style': "display: none;"}),
                                              'fiber': Textarea(attrs={'style': "display: none;"}),
                                              'energy': Textarea(attrs={'style': "display: none;"}),
                                              'category': Textarea(attrs={'style': "display: none;"}),
                                              'cooking_method': Textarea(attrs={'style': "display: none;"}),
                                              'comment': Textarea(attrs={'class': "form-control", 'rows': "3"}),
                                          },
                                          extra=0, )

def get_queryset(date_default):
    queryset: dict = {
        'salad': Product.objects.filter(timetable__datetime=date_default).filter(category='Салаты'),
        'soup': Product.objects.filter(timetable__datetime=date_default).filter(category='Первые блюда'),
        'main_dishes': Product.objects.filter(timetable__datetime=date_default).filter(category='Вторые блюда'),
        'side_dishes': Product.objects.filter(timetable__datetime=date_default).filter(category='Гарниры'),
        'breakfast': Product.objects.filter(timetable__datetime=date_default).filter(category='Завтраки'),
        'porridge': Product.objects.filter(timetable__datetime=date_default).filter(category='Каши'),
            }
    return queryset


def get_formset(queryset, ProductFormSet, request) -> dict:
    if request:
        formset: dict = {
            'salad': ProductFormSet(request.POST, request.FILES, queryset=queryset['salad'], prefix='salad'),
            'soup': ProductFormSet(request.POST, request.FILES, queryset=queryset['soup'], prefix='soup'),
            'main_dishes': ProductFormSet(request.POST, request.FILES, queryset=queryset['main_dishes'], prefix='main_dishes'),
            'side_dishes': ProductFormSet(request.POST, request.FILES, queryset=queryset['side_dishes'], prefix='side_dishes'),
            'breakfast': ProductFormSet(request.POST, request.FILES, queryset=queryset['breakfast'], prefix='breakfast'),
            'porridge': ProductFormSet(request.POST, request.FILES, queryset=queryset['porridge'], prefix='porridge'),
                }
    else:
        formset: dict = {
            'salad': ProductFormSet(queryset=queryset['salad'], prefix='salad'),
            'soup': ProductFormSet(queryset=queryset['soup'], prefix='soup'),
            'main_dishes': ProductFormSet(queryset=queryset['main_dishes'], prefix='main_dishes'),
            'side_dishes': ProductFormSet(queryset=queryset['side_dishes'], prefix='side_dishes'),
            'breakfast': ProductFormSet(queryset=queryset['breakfast'], prefix='breakfast'),
            'porridge': ProductFormSet(queryset=queryset['porridge'], prefix='porridge'),
                }
    return formset

def get_stat_index():
    count_prosucts = len(Product.objects.filter(~Q(category='Блюда от шефа')))
    count_prosucts_labeled = len(Product.objects.filter(
        ~Q(category='Блюда от шефа') |
        Q(ovd='True') | Q(ovd_sugarless='True') | Q(ovd_vegan='True') | Q(shd='True') | Q(shd_sugarless=True) |
        Q(bd='True') | Q(vbd='True') | Q(nbd='True') | Q(nkd='True') | Q(vkd='True') |
        Q(iodine_free='True') | Q(not_suitable='True')))
    count_prosucts_not_labeled = count_prosucts - count_prosucts_labeled
    if count_prosucts != 0:
        progress = int(count_prosucts_labeled * 100 / count_prosucts)
    else:
        progress = 0
    return count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress


@user_passes_test(group_nutritionists_check, login_url='login')
@login_required(login_url='login')
def index(request):
    error = ''
    ProductFormSet = get_modelformset()

    date_default = str(date.today()) if request.method == 'GET' else str(request.POST['datetime'])

    # получение статистики
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat_index()

    queryset: dict = get_queryset(date_default)

    if request.method == 'POST' and 'save' in request.POST:
        form_date = TimetableForm(request.POST)

        formset = get_formset(queryset, ProductFormSet, request)

        if not all([f.is_valid() for f in formset.values()]):
            data = {'formset': formset,
                    'count_prosucts': count_prosucts,
                    'count_prosucts_labeled': count_prosucts_labeled,
                    'count_prosucts_not_labeled': count_prosucts_not_labeled,
                    'form_date': form_date,
                    'progress': progress,
                           }
            return render(request, 'index.html', context=data)
        else:
            for f in formset.values():
                f.save()

            date_default = str(request.POST['datetime'])

            queryset: dict = get_queryset(date_default)

    if request.method == 'POST' and 'find_date' in request.POST:
        form_date = TimetableForm(request.POST)
        if form_date.is_valid():
            date_default = str(form_date.cleaned_data["datetime"])
            queryset: dict = get_queryset(date_default)
            formset = get_formset(queryset, ProductFormSet, None)

            data = {
                'form_date': form_date,
                'error': error,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
            }
            return render(request, 'index.html', context=data)
    else:
        formset = get_formset(queryset, ProductFormSet, None)
        form_date = TimetableForm(initial={'datetime': date_default})
        data = {
            'form_date': form_date,
            'error': error,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
        }
    return render(request, 'index.html', context=data)


@user_passes_test(group_nutritionists_check, login_url='login')
@login_required(login_url='login')
def search(request):
    # load_product()
    error = ''
    ProductFormSet = get_modelformset()
    formset = ''
    queryset = Product.objects.all()
    if request.method == 'POST':
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset)
        if formset.is_valid():
            formset.save()
            queryset = Product.objects.filter(name=formset.data['form-0-name'])
            formset = ProductFormSet(queryset=queryset)
        else:
            error = 'error'
    if request.GET != {}:
        queryset = Product.objects.filter(name=request.GET['search'])
        formset = ProductFormSet(queryset=queryset)
    products = Product.objects.all()
    data = {
        'formset': formset,
        'products': products,
        'error': error,
        }
    return render(request, 'search.html', context=data)

def page_calc(page, count_prosucts):
    page = int(page)
    page_start = page - 25
    page_finish = page - 1
    page_count = math.ceil(count_prosucts / 25)
    page_dict = {item: str(item * 25) for item in range(1, page_count + 1)}
    page_prev = page - 25
    page_next = page + 25
    if page_next > (page_count * 25):
        page_next = 0
    return page_start, page_finish, str(page_prev), str(page_next), page_dict


def get_stat(category):
    count_prosucts = len(Product.objects.filter(category__in=category))
    count_prosucts_labeled = len(Product.objects.filter(category__in=category).filter(
        Q(ovd='True') | Q(ovd_sugarless='True') | Q(ovd_vegan='True') | Q(shd='True') | Q(shd_sugarless=True) |
        Q(bd='True') | Q(vbd='True') | Q(nbd='True') | Q(nkd='True') | Q(vkd='True') |
        Q(iodine_free='True') | Q(not_suitable='True')))
    count_prosucts_not_labeled = count_prosucts - count_prosucts_labeled
    progress = int(count_prosucts_labeled * 100 / count_prosucts)
    return count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress


@login_required(login_url='login')
@user_passes_test(group_nutritionists_check, login_url='login')
def catalog_salad(request, page):
    error = ''
    MEALS: tuple = ('Салаты',)
    ProductFormSet = get_modelformset()
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)

    page_start, page_finish, page_prev, page_next, page_dict = page_calc(page, count_prosucts)
    q = Product.objects.filter(category__in=MEALS).order_by(Lower('name'))[page_start:page_finish + 1]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])
    queryset = queryset.order_by(Lower('name'))

    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='salad')
        if not formset.is_valid():
            return render(request,
                          'salad.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,
                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)
            data = {
                'page': page,
                'page_prev': page_prev,
                'page_next': page_next,
                'page_dict': page_dict,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'salad.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='salad')

        data = {
            'queryset': queryset,
            'page': page,
            'page_prev': page_prev,
            'page_next': page_next,
            'page_dict': page_dict,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'salad.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_nutritionists_check, login_url='login')
def catalog_soup(request, page):
    MEALS: tuple = ('Первые блюда',)
    ProductFormSet = get_modelformset()

    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)

    page_start, page_finish, page_prev, page_next, page_dict = page_calc(page, count_prosucts)
    q = Product.objects.filter(category__in=MEALS).order_by(Lower('name'))[page_start:page_finish + 1]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])
    queryset = queryset.order_by(Lower('name'))

    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='soup')
        if not formset.is_valid():
            return render(request,
                          'soup.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)
            data = {
                'page': page,
                'page_prev': page_prev,
                'page_next': page_next,
                'page_dict': page_dict,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'soup.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='soup')

        data = {
            'page': page,
            'page_prev': page_prev,
            'page_next': page_next,
            'page_dict': page_dict,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'soup.html', context=data)


@login_required
@user_passes_test(group_nutritionists_check, login_url='login')
def catalog_main_dishes(request, page):
    MEALS: tuple = ('Вторые блюда',)
    ProductFormSet = get_modelformset()
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)

    page_start, page_finish, page_prev, page_next, page_dict = page_calc(page, count_prosucts)
    q = Product.objects.filter(category__in=MEALS).order_by(Lower('name'))[page_start:page_finish + 1]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])
    queryset = queryset.order_by(Lower('name'))

    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='main_dishes')
        if not formset.is_valid():
            return render(request,
                          'main_dishes.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)
            data = {
                'page': page,
                'page_prev': page_prev,
                'page_next': page_next,
                'page_dict': page_dict,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
            }
            return render(request, 'main_dishes.html', context=data)
    else:
        formset = ProductFormSet(queryset=queryset, prefix='main_dishes')
        data = {
            'page': page,
            'page_prev': page_prev,
            'page_next': page_next,
            'page_dict': page_dict,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
        }
    return render(request, 'main_dishes.html', context=data)


@login_required
@user_passes_test(group_nutritionists_check, login_url='login')
def catalog_breakfast(request, page):
    ProductFormSet = get_modelformset()
    MEALS: tuple = ('Завтраки', 'Каши')
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)

    page_start, page_finish, page_prev, page_next, page_dict = page_calc(page, count_prosucts)
    q = Product.objects.filter(category__in=MEALS).order_by(Lower('name'))[page_start:page_finish + 1]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])
    queryset = queryset.order_by(Lower('name'))

    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='breakfast')
        if not formset.is_valid():
            return render(request,
                          'breakfast.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)
            data = {
                'page': page,
                'page_prev': page_prev,
                'page_next': page_next,
                'page_dict': page_dict,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
            }
            return render(request, 'breakfast.html', context=data)
    else:
        formset = ProductFormSet(queryset=queryset, prefix='breakfast')
        data = {
            'page': page,
            'page_prev': page_prev,
            'page_next': page_next,
            'page_dict': page_dict,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
        }
    return render(request, 'breakfast.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_nutritionists_check, login_url='login')
def catalog_side_dishes(request, page):
    MEALS: tuple = ('Гарниры',)
    ProductFormSet = get_modelformset()
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)

    page_start, page_finish, page_prev, page_next, page_dict = page_calc(page, count_prosucts)
    q = Product.objects.filter(category__in=MEALS).order_by(Lower('name'))[page_start:page_finish + 1]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])
    queryset = queryset.order_by(Lower('name'))

    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='side_dishes')
        if not formset.is_valid():
            return render(request,
                          'side_dishes.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat(MEALS)
            data = {
                'page': page,
                'page_prev': page_prev,
                'page_next': page_next,
                'page_dict': page_dict,
                'formset': formset,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'side_dishes.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='side_dishes')

        data = {
            'page': page,
            'page_prev': page_prev,
            'page_next': page_next,
            'page_dict': page_dict,
            'formset': formset,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'side_dishes.html', context=data)


class BaseAPIView(APIView):
    def post(self, request):
        data = request.data
        data_str = str(data)
        Base.objects.create(base=data_str)
        data_dict = dict(data)
        js = open("cooking_method.json").read()
        dict_tk = json.loads(js)
        if data_dict['menu']['location']['name'] == 'hadassah':
            load_menu(data_dict, dict_tk)
            load_timetable(data_dict)
            Base.objects.create(base=data_str)
        return Response(data)


class VerifyAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            if Barcodes.objects.get(number=data['barcode']):
                return Response('No')
        except Exception:
            pass
        return Response('Yes')



class DeactivateAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            Barcodes.objects.get(number=data['barcode'])
            return Response('Barcode already deactivated')
        except Exception:
            Barcodes(number=data['barcode'], status='no_active').save()
            return Response('Yes')


def user_login(request):
    test = 'test'
    errors = None
    if request.method == 'POST':
        user_form = UserloginForm(request.POST)
        user = authenticate(username=user_form.data['username'],
                            password=user_form.data['password'])
        if user is not None:
            login(request, user)
            if user.groups.filter(name='nutritionists').exists():
                return HttpResponseRedirect(reverse('index'))
            if user.groups.filter(name='doctors').exists():
                return HttpResponseRedirect(reverse('doctor'))
            if user.groups.filter(name='patients').exists():
                return HttpResponseRedirect(reverse('patient'))
            if user.groups.filter(name='kitchen').exists():
                return HttpResponseRedirect(reverse('printed_form_one_new'))
            if user.groups.filter(name='guest').exists():
                return HttpResponseRedirect(reverse('menu'))
        else:
            errors = 'Пользователь с таким именем или паролем не существует'
    else:
        user_form = UserloginForm()
    return render(request, 'nutritionist/registration/login.html', {'user_form': user_form,
                                                       'errors': errors})


def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    """ Регистрация нового пользователя"""
    errors = []
    if request.method == 'POST':
        password = ''.join([random.choice("123456789qwertyuiopasdfghjklzxcvbnm") for i in range(5)])
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            try:
                user = CustomUser.objects.create_user(user_form.data['email'], user_form.data['email'], password)
                # def chk_rest(s):
                #     pat = r'([^а-яА-Яa-zA-Z0-9ёЁ\)\(-\' .,])'
                #     return re.findall(pat, flags=re.I)
                user.first_name = user_form.data['name']
                user.last_name = user_form.data['lastname']
                group_nutritionists = Group.objects.get(name='doctors')
                group_nutritionists.user_set.add(user)
                user.save()
                text_email = f"<p>Регистрация прошла успешно!</p>\
                            <p>логин: {user_form.data['email']}</p> \
                            <p>пароль: {password}</p> \
                            <p>Для авторизации пройдите по ссылке \
                            <a href='https://sk.petrushkagroup.ru/login/'>sk.petrushkagroup.ru/login/</a></p>"

                send_mail(
                    'Регистрация в личном кабинете врача.',
                    text_email,
                    'info@petrushkagroup.ru',
                    [user_form.data['email']],
                    fail_silently=False,
                    html_message=text_email,
                )

                return render(request, 'nutritionist/registration/register_done.html', {'user_form': user_form, 'errors': errors})
            except Exception:
                errors.append('Пользователь с такой почтой уже существует')
                return render(request, 'nutritionist/registration/register.html',
                              {'user_form': user_form, 'errors': errors})


    user_form = UserRegistrationForm()
    return render(request, 'nutritionist/registration/register.html', {'user_form': user_form, 'errors': errors})


def password_reset(request):
    """ Сброс пароля """
    errors = []
    password = ''.join([random.choice("123456789qwertyuiopasdfghjklzxcvbnm") for i in range(5)])
    if request.method == 'POST':
        user_form = UserPasswordResetForm(request.POST)
        if user_form.is_valid():
            try:
                user = CustomUser.objects.get(email=user_form.data['email'])
                user.set_password(password)
                user.save()
                text_email = f"<p>Сброс пароля прошел успешно!</p>\
                            <p>логин: {user_form.data['email']}</p> \
                            <p>пароль: {password}</p> \
                            <p>Для авторизации пройдите по ссылке \
                            <a href='https://sk.petrushkagroup.ru/login/'>sk.petrushkagroup.ru/login/</a></p>"
                send_mail(
                    'Сброс пароля',
                    text_email,
                    'info@petrushkagroup.ru',
                    [user_form.data['email']],
                    fail_silently=False,
                    html_message=text_email,
                )
                return render(request, 'nutritionist/registration/password_reset_done.html', {'user_form': user_form, 'errors': errors})
            except Exception:
                errors.append('Пользователь с такой почтой не зарегистророван')
    else:
        user_form = UserPasswordResetForm()
    return render(request, 'nutritionist/registration/password_reset_email.html', {'user_form': user_form, 'errors': errors})

def manager(request):
    patients = CustomUser.objects.filter(status='patient').order_by('full_name').values('id', 'full_name')
    return render(request, 'admin.html', context={'patients': patients})


def edit_photo(request, product_id, type):
    """Редактировать фотографию блюда"""


    if request.method == "POST":
        product_id = request.POST['product_id']
        link = f'/admin/nutritionist/productlp/{product_id}/change/'

        return HttpResponseRedirect(link)

    product = ProductLp.objects.get(id=product_id)

    data = {
        'product_id': product_id,
        'image': product.image if type == "full" else product.image_min,
        'type': type
    }

    return render(request, 'edit_photo.html', context=data)
def admin_foods(request):
    """Админ-панель для внесения изменений в приемы пищи пациента"""
    patient = CustomUser.objects.filter(status='patient').order_by('full_name').first()

    data = {
        'full_name': patient.full_name,
        'diet': patient.type_of_diet,
        'comment': patient.comment,
        'date': str(date.today()),
        'user_id': patient.id,
    }
    return render(request, 'foods.html', context=data)


def admin_foods_new(request):
    """Админ-панель для внесения изменений в приемы пищи пациента"""
    patient = CustomUser.objects.filter(status='patient').order_by('full_name').first()
    today = str(date.today())
    tomorrow = str(date.today() + timedelta(days=1))
    day_after_tomorrow = str(date.today() + timedelta(days=2))
    day_date = {
        'today': {
            'short': today,
            'full': dateformat.format(date.fromisoformat(today), 'd E, l').lower()},
        'tomorrow':
            {'short': tomorrow,
             'full': dateformat.format(date.fromisoformat(tomorrow), 'd E, l').lower()},
        'day_after_tomorrow':
            {'short': day_after_tomorrow,
             'full': dateformat.format(date.fromisoformat(day_after_tomorrow), 'd E, l').lower()},
    }

    data = {
        'full_name': patient.full_name,
        'diet': patient.type_of_diet,
        'comment': patient.comment,
        'date': str(date.today()),
        'user_id': patient.id,
        'sort_field': 'full_name',
        'day_date': day_date
    }
    return render(request, 'foods-new.html', context=data)

def photo_statistics(request):
    """Статистика по блюдам с фотографиями"""
    count_products = ProductLp.objects.filter(status=1).count()
    count_products_with_photo = ProductLp.objects.filter(~Q(image=None) & ~Q(image="")).count()

    data = {
        'percentage_of_completion': round((100 * count_products_with_photo / count_products), 1),
        'count_products': str(count_products),
        'count_products_with_photo': str(count_products_with_photo),
    }
    return render(request, 'photo_statistics.html', context=data)

def printed_form_one_new(request):
    is_public = False  # выводим технические названия блюд, не публичные
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    floors = {
    'second': ['2а-1', '2а-2', '2а-3', '2а-4', '2а-5', '2а-6', '2а-7', '2а-8', '2а-9', '2а-10', '2а-11', '2а-12', '2а-13',
               '2а-14', '2а-15', '2а-16', '2а-17'],
    'third': ['3а-1', '3а-2', '3а-3', '3а-4', '3а-5', '3а-6', '3а-7', '3а-8', '3а-9', '3а-10', '3а-11',
                    '3а-12', '3а-13', '3а-14', '3а-15', '3а-16', '3а-17', '3b-1', '3b-2', '3b-3', '3b-4',
                    '3b-5', '3b-6', '3b-7', '3b-8', '3b-9', '3b-10'],
    'fourtha': ['4а-1', '4а-2', '4а-3', '4а-4', '4а-5', '4а-6', '4а-7', '4а-8', '4а-9', '4а-10', '4а-11',
                      '4а-12', '4а-13', '4а-14', '4а-15', '4а-16'],
    }
    time_now = datetime.today().time().strftime("%H:%M")
    # какой прием пищи
    meal, day = what_meal() # после return 'breakfast', 'tomorrow'
    type_order = what_type_order()
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    if type_order == 'flex-order':
        users = UsersToday.objects.all()
    else:
        users = UsersReadyOrder.objects.all()

    catalog = {'meal': translate_meal(meal),
               'count': users.count(),
               'count_2nd_floor': users.filter(floor='2').count(),
               'count_3nd_floor': users.filter(floor='3').count(),
               'count_4nd_floor': users.filter(floor='4').count(),
               'count_not_floor': users.filter(floor='Не выбрано').count(),
               'count_diet': counting_diets(users, floors),
               'users_2nd_floor': create_list_users_on_floor(users, '2', meal, date_create, type_order, is_public),
               'users_3nd_floor': create_list_users_on_floor(users, '3', meal, date_create, type_order, is_public),
               'users_4nd_floor': create_list_users_on_floor(users, '4', meal, date_create, type_order, is_public),
               'users_not_floor': create_list_users_on_floor(users, 'Не выбрано', meal, date_create, type_order, is_public),
               }
    number = 0
    count_users_with_cafe_prod = 0
    # расставляем порядковые номера и считаем кол-во пациетнов с блюдами с кафе
    for user in catalog['users_2nd_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1
    for user in catalog['users_3nd_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1
    for user in catalog['users_4nd_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1
    for user in catalog['users_not_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1

    data = {
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'count_users_with_cafe_prod': count_users_with_cafe_prod,
        'day': day,
        'date_create': dateformat.format(date.fromisoformat(str(date_create)), 'd E')
    }

    return render(request, 'printed_form1_new.html', context=data)

def printed_form_one(request):
    is_public = False  # выводим технические названия блюд, не публичные
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    floors = {
    'second': ['2а-1', '2а-2', '2а-3', '2а-4', '2а-5', '2а-6', '2а-7', '2а-8', '2а-9', '2а-10', '2а-11', '2а-12',
               '2а-13', '2а-14', '2а-15', '2а-16', '2а-17'],
    'third': ['3а-1', '3а-2', '3а-3', '3а-4', '3а-5', '3а-6', '3а-7', '3а-8', '3а-9', '3а-10', '3а-11',
                    '3а-12', '3а-13', '3а-14', '3а-15', '3а-16', '3а-17', '3b-1', '3b-2', '3b-3', '3b-4',
                    '3b-5', '3b-6', '3b-7', '3b-8', '3b-9', '3b-10'],
    'fourtha': ['4а-1', '4а-2', '4а-3', '4а-4', '4а-5', '4а-6', '4а-7', '4а-8', '4а-9', '4а-10', '4а-11',
                      '4а-12', '4а-13', '4а-14', '4а-15', '4а-16'],
    }
    time_now = datetime.today().time().strftime("%H:%M")
    # какой прием пищи
    meal, day = what_meal() # после return 'breakfast', 'tomorrow'
    type_order = what_type_order()
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    if type_order == 'flex-order':
        users = UsersToday.objects.all()
    else:
        users = UsersReadyOrder.objects.all()

    catalog = {'meal': translate_meal(meal),
               'count': len(users),
               'count_2nd_floor': len([user for user in users if user.room_number in floors['second']]),
               'count_3nd_floor': len([user for user in users if user.room_number in floors['third']]),
               'count_4nd_floor': len([user for user in users if user.room_number in floors['fourtha']]),
               'count_not_floor': len([user for user in users if user.room_number in ['Не выбрано']]),
               'count_diet': counting_diets(users, floors),
               'users_2nd_floor': create_list_users_on_floor(users, floors['second'], meal, date_create, type_order, is_public),
               'users_3nd_floor': create_list_users_on_floor(users, floors['third'], meal, date_create, type_order, is_public),
               'users_4nd_floor': create_list_users_on_floor(users, floors['fourtha'], meal, date_create, type_order, is_public),
               'users_not_floor': create_list_users_on_floor(users, ['Не выбрано'], meal, date_create, type_order, is_public),
               }
    number = 0
    count_users_with_cafe_prod = 0
    # расставляем порядковые номера и считаем кол-во пациетнов с блюдами с кафе
    for user in catalog['users_2nd_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1
    for user in catalog['users_3nd_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1
    for user in catalog['users_4nd_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1
    for user in catalog['users_not_floor']:
        number += 1
        user['number'] = str(number)
        if len(user['products_cafe']) > 0:
            count_users_with_cafe_prod += 1

    data = {
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'count_users_with_cafe_prod': count_users_with_cafe_prod,
        'day': day,
        'date_create': dateformat.format(date.fromisoformat(str(date_create)), 'd E')
    }

    return render(request, 'printed_form1.html', context=data)


def printed_form_two_lp(request):
    is_public = False  # выводим технические названия блюд, не публичные
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = str(datetime.today().time().hour) + ':' + str(datetime.today().time().minute)
    # какой прием пищи
    meal, day = what_meal() # после return 'breakfast', 'tomorrow'
    type_order = what_type_order()
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    catalog = {}

    if type_order == 'flex-order':
        users = UsersToday.objects.all()
    else:
        users = UsersReadyOrder.objects.all()
    # users = users.filter(status='patient').filter(receipt_date__lte=date.today())
    for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
        list_whith_unique_products = []
        for diet in ['ОВД', 'ОВД без сахара', 'ЩД', 'ЩД без сахара',
                     'ОВД веган (пост) без глютена', 'Нулевая диета',
                     'БД', 'ВБД', 'НБД', 'НКД', 'ВКД', 'БД день 1',
                     'БД день 2', 'Безйодовая', 'ПЭТ/КТ', 'Без ограничений']:
            users_with_diet = users.filter(type_of_diet=diet)
            all_products = [] # стовляем список всех продуктов
            comment_list = []
            for user in users_with_diet:
                if type_order == 'flex-order':
                    menu_all = MenuByDay.objects.filter(user_id=user.user_id)
                else:
                    menu_all = MenuByDayReadyOrder.objects.filter(user_id=user.id)
                # if category == 'products' or category ==  'drink':
                #     pr = check_value_two(menu_all, str((date_create)), meal, category, is_public)
                if category == 'soup':
                    pr = check_value_two(menu_all, str((date_create)), meal, 'soup', user.id, is_public) + \
                         check_value_two(menu_all, str((date_create)), meal, 'bouillon', user.id, is_public)
                    try:
                        pr.remove(None)
                    except:
                        pass
                else:
                    pr = check_value_two(menu_all, str((date_create)), meal, category, user.id, is_public)
                # if pr != None:
                #     all_products.append(pr)
                if pr[0] not in [None, [None]]:
                    for item in pr:
                        item['comment'] = add_features(user.comment,
                             user.is_probe,
                             user.is_without_salt,
                             user.is_without_lactose,
                             user.is_pureed_nutrition)
                        all_products.append(item)
            # составляем список с уникальными продуктами
            unique_products = []
            for product in all_products:
                flag = True
                for un_product in unique_products:
                    if product != None or un_product != None:
                        if product['id'] == un_product['id']:
                            flag = False
                if flag == True:
                    if product:
                        if 'cafe' not in product['id']:
                            unique_products.append(product)
            # добавляем элеметны списока с уникальными продуктами, кол-вом(сколько продуктов всего)
            # типом диеты
            for un_product in unique_products:
                count = 0
                for product in all_products:
                    if product['id'] == un_product['id']:
                        count += 1
                        comment_list.append(product['comment'])
                un_product['count'] = str(count)
                un_product['diet'] = diet
                if '' in comment_list:
                    comment_list.sort()
                comment_set = set(comment_list)
                comment_list_dict = [{'comment': f'{"Без комментария." if item == "" else item}', 'count': comment_list.count(item)} for item in comment_set]

                un_product['comments'] = comment_list_dict

            # list_whith_unique_products.append(unique_products)
            [list_whith_unique_products.append(item) for item in unique_products]
        catalog[category] = list_whith_unique_products

    for cat in catalog.values():
        for i, pr in enumerate(cat):
            for ii in range(i + 1, len(cat)):
                if pr != None and cat[ii] != None:
                    if pr['id'] == cat[ii]['id']:
                        pr['count'] = str(int(pr['count']) + int(cat[ii]['count']))
                        pr['diet'] = pr['diet'] + ', ' + cat[ii]['diet']
                        pr['comments'] = pr['comments'] + cat[ii]['comments']
                        cat[ii] = None

    for item in catalog.values():
        for product in item:
            if product != None:
                catalog_key_set = list(set([item['comment'] for item in product['comments']]))
                if 'Без комментария.' in catalog_key_set:
                    catalog_key_set.remove('Без комментария.')
                    catalog_key_set.insert(0, 'Без комментария.')
                result = []
                if 'Без комментария.' in catalog_key_set:
                    catalog_key_set
                for key in catalog_key_set:
                    result.append({'comment': key,
                                   'count': sum([item['count'] for item in product['comments'] if key == item['comment']])})
                product['comments'] = result

    data = {
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'day': day,
        'date_create': date_create,
        'meal': translate_meal(meal)
    }
    return render(request, 'printed_form2_lp.html', context=data)

def printed_form_two_lp_new(request):
    """ Отчет для цеха лечебного питания.  """
    is_public = False  # выводим технические названия блюд, не публичные
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = str(datetime.today().time().hour) + ':' + str(datetime.today().time().minute)
    # какой прием пищи
    meal, day = what_meal() # после return 'breakfast', 'tomorrow'
    type_order = what_type_order()
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    delta_day = "-1" if day == 'tomorrow' else "0"
    catalog = {}

    if type_order == 'flex-order':
        users = UsersToday.objects.all()
    else:
        users = UsersReadyOrder.objects.all()
    # users = users.filter(status='patient').filter(receipt_date__lte=date.today())
    for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
        list_whith_unique_products = []
        for diet in ['ОВД', 'ОВД без сахара', 'ЩД', 'ЩД без сахара',
                     'ОВД веган (пост) без глютена', 'Нулевая диета',
                     'БД', 'ВБД', 'НБД', 'НКД', 'ВКД', 'БД день 1',
                     'БД день 2', 'Безйодовая', 'ПЭТ/КТ', 'Без ограничений']:
            users_with_diet = users.filter(type_of_diet=diet)
            all_products = [] # стовляем список всех продуктов
            comment_list = []
            for user in users_with_diet:
                if type_order == 'flex-order':
                    menu_all = MenuByDay.objects.filter(user_id=user.user_id)
                else:
                    menu_all = MenuByDayReadyOrder.objects.filter(user_id=user.id)
                # if category == 'products' or category ==  'drink':
                #     pr = check_value_two(menu_all, str((date_create)), meal, category, is_public)
                if category == 'soup':
                    pr = check_value_two(menu_all, str((date_create)), meal, 'soup', user.id,  is_public) + \
                        check_value_two(menu_all, str((date_create)), meal, 'bouillon', user.id,  is_public)
                    try:
                        pr.remove(None)
                    except:
                        pass
                else:
                    pr = check_value_two(menu_all, str((date_create)), meal, category, user.id, is_public)
                # if pr != None:
                #     all_products.append(pr)
                if pr[0] not in [None, [None]]:
                    for item in pr:
                        item['comment'] = add_features(user.comment,
                             user.is_probe,
                             user.is_without_salt,
                             user.is_without_lactose,
                             user.is_pureed_nutrition)
                        all_products.append(item)
            # составляем список с уникальными продуктами
            #
            unique_products = []
            for product in all_products:
                flag = True
                for un_product in unique_products:
                    if product != None or un_product != None:
                        if product['id'] == un_product['id']:
                            flag = False
                if flag == True:
                    if product:
                        if 'cafe' not in product['id']:
                            unique_products.append(product)
            # добавляем элеметны списока с уникальными продуктами, кол-вом(сколько продуктов всего)
            # типом диеты
            for un_product in unique_products:
                count = 0
                comment_list = []
                for product in all_products:
                    if product['id'] == un_product['id']:
                        count += 1
                        comment_list.append(product['comment'])
                un_product['count'] = str(count)
                # un_product['diet'] = diet
                un_product.setdefault('diet', []).append(diet)
                if '' in comment_list:
                    comment_list.sort()
                comment_set = set(comment_list)
                comment_list_dict = [{'comment': f'{"Без комментария." if item == "" else item}', 'count': comment_list.count(item)} for item in comment_set]

                un_product['comments'] = comment_list_dict

            # list_whith_unique_products.append(unique_products)
            [list_whith_unique_products.append(item) for item in unique_products]
        catalog[category] = list_whith_unique_products

    for cat in catalog.values():
        for i, pr in enumerate(cat):
            for ii in range(i + 1, len(cat)):
                if pr != None and cat[ii] != None:
                    if pr['id'] == cat[ii]['id']:
                        pr['count'] = str(int(pr['count']) + int(cat[ii]['count']))
                        # pr['diet'] = pr['diet'] + ', ' + cat[ii]['diet']
                        for item in cat[ii]['diet']:
                            pr.setdefault('diet', []).append(item)
                        pr['comments'] = pr['comments'] + cat[ii]['comments']
                        cat[ii] = None
    # обьединяем доп. бульон и бульон и удаляем None
    soups = [soup for soup in catalog['soup'] if soup]
    soups = combine_broths(soups)
    catalog['soup'] = soups

    for item in catalog.values():
        for product in item:
            if product != None:
                catalog_key_set = list(set([item['comment'] for item in product['comments']]))
                if 'Без комментария.' in catalog_key_set:
                    catalog_key_set.remove('Без комментария.')
                    catalog_key_set.insert(0, 'Без комментария.')
                result = []
                if 'Без комментария.' in catalog_key_set:
                    catalog_key_set
                for key in catalog_key_set:
                    result.append({'comment': key,
                                   'count': sum([item['count'] for item in product['comments'] if key == item['comment']])})
                product['comments'] = result

    number = 0
    for item in catalog.values():
        for product in item:
            if product != None:
                number += 1
                product['number'] = number
                product['diet'] = {
                    'many': len(product['diet']) > 1,
                    'diet': [{'name': pr} for pr in product['diet']]
                }

    data = {
        'type': 'Цех лечебного питания',
        'title': 'Заявка для цеха лечебного питания',
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'day': day,
        'date_create': date_create,
        'meal': translate_meal(meal),
        'meal_en': meal,
        'delta_day': delta_day
    }
    return render(request, 'printed_form2_lp_new.html', context=data)


def printed_form_two_cafe(request):
    """ Заявка по блюдам линии раздачи. """
    is_public = False  # выводим технические названия блюд, не публичные
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = datetime.today().time().strftime("%H:%M")
    meal, day = what_meal()  # после return 'breakfast', 'tomorrow'
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    catalog = {}

    for meal in ['breakfast', 'lunch', 'dinner']:
        # Проверяем сформирован ли прием пищи
        is_ready_meal, patients = checking_is_ready_meal(meal)
        category_dict = create_category_dict(meal, is_ready_meal, patients)
        # Добавляем порядковые номера блюд и переводим тип диеты в формат для вывода в заявке
        category_dict = complete_catalog(category_dict)
        catalog[meal] = category_dict

    catalog = cleaning_null(catalog)

    data = {
        'type': 'Цех линии раздачи',
        'title': 'Заявка по блюдам раздачи',
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalogs': catalog,
        'day': day,
        'date_create': date_create,
    }
    return render(request, 'printed_form2_cafe.html', context=data)

def printed_form_two_cafe_new(request):
    """ Заявка по блюдам линии раздачи. """
    is_public = False  # выводим технические названия блюд, не публичные
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = datetime.today().time().strftime("%H:%M")
    meal, day = what_meal()  # после return 'breakfast', 'tomorrow'
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    catalog = {}

    for meal in ['breakfast', 'lunch', 'dinner']:
        # Проверяем сформирован ли прием пищи
        is_ready_meal, patients = checking_is_ready_meal(meal)
        category_dict = create_category_dict(meal, is_ready_meal, patients)
        # Добавляем порядковые номера блюд и переводим тип диеты в формат для вывода в заявке
        category_dict = complete_catalog(category_dict)
        catalog[meal] = category_dict

    catalog = cleaning_null(catalog)

    data = {
        'type': 'Цех линии раздачи',
        'title': 'Заявка по блюдам раздачи',
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalogs': catalog,
        'day': day,
        'date_create': date_create,
    }
    return render(request, 'printed_form2_cafe_new.html', context=data)

def tk(request, id, count):
    import operator
    from nutritionist.models import Ingredient
    count: int = int(count) + 2 if count != '0' else 1  # сутчная проба и бракераж

    tk, error = get_tk(id)

    for item_tk_1 in tk['assemblyCharts']:
        try:
            item_tk_1['name'] = Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().name
        except:
            item_tk_1['name'] = get_name(item_tk_1['assembledProductId'])

        try:
            item_tk_1['weight'] =\
                Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().weight * 1000
        except:
            item_tk_1['weight'] = 0

        item_tk_1['measure_unit'] = get_measure_unit(item_tk_1['assembledProductId'])

        for item_tk_2 in item_tk_1['items']:
            try:
                item_tk_2['name'] = Ingredient.objects.filter(product_id=item_tk_2['productId']).first().name
            except:
                item_tk_2['name'] = get_name(item_tk_2['productId'])

            # try:
            #     item_tk_2['measure_unit'] = \
            #         Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().measureUnit
            # except:
            item_tk_2['measure_unit'] = get_measure_unit(item_tk_2['productId'])

# # Высчитываем вес с учетом того, что некоторые ТК указаны на определенное кол-во порций
    for item_tk_1 in tk['assemblyCharts']:
        count_por = item_tk_1['assembledAmount']
        for sub_item in item_tk_1['items']:
            sub_item['amountIn'] = sub_item['amountIn'] / count_por
            sub_item['amountMiddle'] = sub_item['amountMiddle'] / count_por
            sub_item['amountOut'] = sub_item['amountOut'] / count_por


# Проставляем имена для preparedCharts
#     for item_tk_1 in tk['preparedCharts']:
#         try:
#             item_tk_1['name'] = Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().name
#         except:
#             item_tk_1['name'] = None
#
#         try:
#             item_tk_1['weight'] =\
#                 Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().weight * 1000
#         except:
#             item_tk_1['weight'] = 0
#
#         for item_tk_2 in item_tk_1['items']:
#             try:
#                 item_tk_2['name'] = Ingredient.objects.filter(product_id=item_tk_2['productId']).first().name
#             except:
#                 item_tk_2['name'] = None

    try:
        result = tk['assemblyCharts'][0]
    except:
        result = "Нет данных"

    if result != "Нет данных":
        for ing in result['items']:
            for ing2 in tk['assemblyCharts'][1:]:
                try:
                    if ing['productId'] == ing2['assembledProductId']:
                        ing['items'] = ing2['items'].copy()
                except:
                    pass
            if 'items' not in ing:
                ing['items'] = None

        result['allergens'] = get_allergens(id)

        for item in result['items']:
            if item['items']:
                item['weight_tk'] = get_weight_tk(item['productId'])
                for sub_item in item['items']:
                    sub_item['amountIn'] = item['amountIn'] * sub_item['amountIn']
                    sub_item['amountMiddle'] = item['amountMiddle'] * sub_item['amountMiddle']
                    sub_item['amountOut'] = item['amountOut'] * sub_item['amountOut']

        result['items'].sort(key=operator.itemgetter('sortWeight'))

        weight = count * int(result['weight'])
    else:
        weight = 0

    try:
        img = ProductLp.objects.filter(product_id=id).first().image
    except:
        img = None



    data = {
        'img': img,
        'result': result,
        'error': error,
        'count': count,
        'weight': weight,
    }
    return render(request, 'tk.html', context=data)



def report(request):
    return render(request, 'report.html', {})


def internal_report(request):
    if request.method == 'GET' and request.GET != {}:
        date_start = parse(request.GET['start'])
        date_finish = parse(request.GET['finish'])
    else:
        date_start = datetime(datetime.today().year, datetime.today().month, 1).date()
        date_finish = datetime.today().date()
    filtered_report = Report.objects.filter(date_create__gte=date_start, date_create__lte=date_finish)

    report = {}
    for index, item in enumerate(filtered_report):
        if 'cafe' in item.product_id:
            try:
                product = Product.objects.get(id=item.product_id.split('-')[2])
                report.setdefault(item.product_id, []).append(
                    {'category': product.category,
                     'name': product.name,
                     })
            except ValueError:
                pass
        else:
            if ',' in item.product_id:
                for id in item.product_id.split(','):
                    try:
                        product = ProductLp.objects.get(id=id)
                        report.setdefault(id, []).append(
                            {'category': product.category,
                             'name': product.name,
                             })
                    except:
                        pass
            else:
                try:
                    product = ProductLp.objects.get(id=item.product_id)
                    report.setdefault(item.product_id, []).append(
                        {'category': product.category,
                         'name': product.name,
                         })
                except:
                    pass

    temporary_report = []
    for item in report.values():
        item[0]['count'] = len(item)
        temporary_report.append(item[0])


    temporary_report.sort(key=operator.itemgetter('category'))
    category = ['гарнир', 'десерт', 'напиток', 'основной', 'салат', 'суп', 'фрукты', 'каша', 'товар', 'hidden']
    intermediate_option = []
    report = []
    for cat in category:
        for item in temporary_report:
            if item['category'] == cat:
                intermediate_option.append(item)
        intermediate_option.sort(key=operator.itemgetter('name'))
        report += intermediate_option
        intermediate_option = []
    for index, item in enumerate(report):
        item['category'] = item['category'] if item['category'] != 'основной' else 'основное'
        item['number'] = index + 1
    add_try(report) # добавляем суточные пробы

    date = {'report': report,
            'date_start': date_start,
            'date_finish': date_finish}
    return render(request, 'internal_report.html', context=date)


def weight_meal(meal):
    MEALS = {
        'breakfast': 0,
        'lunch': 1,
        'afternoon': 2,
        'dinner': 3,
    }
    return MEALS[meal]

# 888
class DownloadReportAPIView(APIView):
    def post(self, request):
        serializer = DownloadReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        # date_start = data['start']
        # date_finish = data['finish']
        date_start = str(data['start'])
        date_finish = str(data['finish'])
        # создать запись что пошел поцесс создания отчета
        id = IsReportCreate.objects.create(is_report_create=False).id
        create_report_download.delay(date_start, date_finish, id)
        # create_report_download(date_start, date_finish, id)

        response = {"response": str(id)}
        response = json.dumps(response)

        return Response(response)


class CheckIsReportAPIView(APIView):
    def post(self, request):
        data = request.data
        id = data['id']['response']
        response = {"response": 'no'}
        item = IsReportCreate.objects.filter(id=id)
        if item.exists():
            if item.first().is_report_create:
                response = {"response": 'yes'}

        response = json.dumps(response)
        return Response(response)


def create_сatalog(is_public, meal, patient, day):
    """ Создание словаря этикеток. """

    # floors = {
    # 'second': ['2а-1', '2а-2', '2а-3', '2а-4', '2а-5', '2а-6', '2а-7', '2а-12', '2а-13', '2а-14', '2а-15',
    #                  '2а-16', '2а-17'],
    # 'third': ['3а-1', '3а-2', '3а-3', '3а-4', '3а-5', '3а-6', '3а-7', '3а-8', '3а-9', '3а-10', '3а-11',
    #                 '3а-12', '3а-13', '3а-14', '3а-15', '3а-16', '3а-17', '3b-1', '3b-2', '3b-3', '3b-4',
    #                 '3b-5', '3b-6', '3b-7', '3b-8', '3b-9', '3b-10'],
    # 'fourtha': ['4а-1', '4а-2', '4а-3', '4а-4', '4а-5', '4а-6', '4а-7', '4а-8', '4а-9', '4а-10', '4а-11',
    #                   '4а-12', '4а-13', '4а-14', '4а-15', '4а-16'],
    # }

    # какой прием пищи
    # meal, day = what_meal() # после return 'breakfast', 'tomorrow'
    # если прием пищи не равер now_meal тогда всегда flex-order
    meal_now, day_now = what_meal()
    # если выбранный прием пищи совпадает с текущим (настоящее)
    if (meal, day) == (meal_now, day_now):
        type_order = what_type_order()
        type_time = None
    # если выбранный прием пищи раньше текущего (прошлое)
    elif weight_meal(meal) < weight_meal(meal_now):
        # type_order = 'report-order'
        # 555
        type_order = 'flex-order'
        type_time = 'past'
    # если выбранный прием пищи позже текущего (будущее)
    elif weight_meal(meal) > weight_meal(meal_now):
        type_order = 'flex-order'
        type_time = 'future'

    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()

    filter_patients = Q() if patient == 'all' else Q(user_id=patient)
    if type_order == 'flex-order' and not type_time:
        users = UsersToday.objects.filter(filter_patients)
    if type_order == 'flex-order' and type_time == 'past' or type_time == 'future':
        users = MenuByDay.objects.filter(
            date=date_create,
            meal=meal,
        ).filter(
            filter_patients
        ).values('user_id').distinct('user_id')
        users = CustomUser.objects.filter(id__in=users)
    elif type_order == 'fix-order':
        users = UsersReadyOrder.objects.filter(filter_patients)
    elif type_order == 'report-order':
        users = Report.objects.filter(
            date_create=date_create,
            meal=meal,
        ).filter(
            filter_patients
        ).values('user_id').distinct('user_id')
        users = CustomUser.objects.filter(id__in=users)



    catalog = {'meal': translate_meal(meal),
               'users_not_floor': create_list_users_on_floor(users, 'Не выбрано', meal, date_create, type_order,
                                                             is_public, type_time),
               'users_2nd_floor': create_list_users_on_floor(users, "2", meal, date_create, type_order, is_public, type_time),
               'users_3nd_floor': create_list_users_on_floor(users, "3", meal, date_create, type_order, is_public, type_time),
               'users_4nd_floor': create_list_users_on_floor(users, "4", meal, date_create, type_order, is_public, type_time),
               }

    return catalog

class CreateStickers(APIView):
    def post(self, request):
        is_public = True  # используем публичные названия для блюд
        meal = request.data['meal']
        meal, day = what_meal() if meal == 'now_meal' else (meal, None)
        patient = request.data['patient']
        try:
            catalog = create_сatalog(is_public, meal, patient, day)
            create_stickers_pdf(catalog)
        except:
            response = {"response": "no"}
            response = json.dumps(response)
            return Response(response)
        response = {"response": "yes"}
        response = json.dumps(response)
        return Response(response)

def get_total_energy_value(day_of_the_week, translated_diet):
    """Возвращает суммарное КБЖУ за день."""
    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet))

    carbohydrate, fat, fiber, energy = 0, 0, 0, 0
    for product in products:
        try:
            carbohydrate += round((float(product.carbohydrate) * float(product.weight) * 10), 2)
        except:
            carbohydrate += 0
        try:
            fat += round((float(product.fat) * float(product.weight) * 10), 2)
        except:
            fat += 0
        try:
            fiber += round((float(product.fiber) * float(product.weight) * 10), 2)
        except:
            fiber += 0
        try:
            energy += round((float(product.energy) * float(product.weight) * 10), 2)
        except:
            energy += 0
    return f'Б - {round(fiber, 2)}, Ж - {round(fat, 2)}, У - {round(carbohydrate, 2)}, Ккал - {round(energy, 2)}'





def get_energy_value(product):
    """Возвращает КБЖУ продукта на порцию"""
    try:
        carbohydrate = round((float(product.carbohydrate) * float(product.weight) * 10), 2)
        fat = round((float(product.fat) * float(product.weight) * 10), 2)
        fiber = round((float(product.fiber) * float(product.weight) * 10), 2)
        energy = round((float(product.energy) * float(product.weight) * 10), 2)
        energy_value = f'Б - {fiber}, Ж - {fat}, У - {carbohydrate}, Ккал - {energy}'
    except:
        energy_value = "Нет данных"
    return energy_value

def creating_meal_menu_lp_new(day_of_the_week, translated_diet, meal):
    if day_of_the_week == 'день 1':
        day_of_the_week = 'понедельник'
    if day_of_the_week == 'день 2':
        day_of_the_week = 'вторник'
    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))

    products_porridge = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                         for product in products.filter(category='каша')]
    products_salad = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                         for product in products.filter(category='салат')]
    products_soup = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                     for product in products.filter(category='суп')]
    products_main = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                     for product in products.filter(category='основной')]
    products_garnish = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                        for product in products.filter(category='гарнир')]
    products_dessert = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                        for product in products.filter(category='десерт')]
    products_fruit = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                      for product in products.filter(category='фрукты')]
    products_drink = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                      for product in products.filter(category='напиток')]
    products_product = [{'name': product.name, 'product_id': product.product_id, 'energy_value':get_energy_value(product)}
                        for product in products.filter(category='товар')]

    all_products = products_salad,\
        products_soup,\
        products_main,\
        products_garnish,\
        products_porridge,\
        products_dessert,\
        products_fruit,\
        products_drink,\
        products_product
    result = []
    for products in all_products:
        for product in products:
            result.append(product)
    return result

def menu_lp_for_staff(request):
    try:
        diet =request.GET['diet']
        day_of_the_week = request.GET['day']
        if day_of_the_week == 'вся неделя':
            DAY_OF_THE_WEEK = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        else:
            DAY_OF_THE_WEEK = [day_of_the_week]
    except:
        diet = 'ОВД'
        day_of_the_week = 'вся неделя'
        DAY_OF_THE_WEEK = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    MEALS = ['breakfast', 'lunch', 'afternoon', 'dinner']
    if diet == 'БД':
        DAY_OF_THE_WEEK = ['день 1', 'день 2']
    menu = {}
    for day in DAY_OF_THE_WEEK:
        menu[day.capitalize()] = {}
        for meal in MEALS:
            meal_in_russian = translate_meal(meal)
            menu[day.capitalize()][meal_in_russian] = creating_meal_menu_lp_new(day, diet, meal)
        menu[day.capitalize()]['Общий КБЖУ'] = get_total_energy_value(day, diet)
    data = {'menu': menu, 'diet': diet, 'day_of_the_week': day_of_the_week}

    return render(request, 'menu_lp_for_staff.html', context=data)