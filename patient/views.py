from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from doctor.forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, CommentProduct, BotChatId
from nutritionist.forms import TimetableForm
import random, calendar, datetime, logging
from datetime import datetime, date, timedelta
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat
from dateutil.parser import parse
from django.db.models.functions import Lower
from doctor.functions.functions import sorting_dishes, parsing, creating_meal_menu_cafe,\
    creating_meal_menu_lp, creates_dict_with_menu_patients_on_day
from patient.functions import formation_menu, creating_menu_for_patient, create_category, create_patient_select,\
    date_menu_history, check_is_comment
from doctor.functions.translator import get_day_of_the_week, translate_diet
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
import telepot, json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from doctor.tasks import my_job_send_messang_changes
from doctor.functions.bot import formatting_full_name

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)


def group_patient_check(user):
    return user.groups.filter(name='patients').exists()


# @login_required
# @user_passes_test(group_patient_check, login_url='login')
def patient(request, id):
    is_public = True  # используем публичные названия блюд
    is_have = 'ok'
    logging.info(f'На странице ЛК пациента')

    date_menu = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + timedelta(days=2)),
    }

    user = CustomUser.objects.get(id=id)
    diet = translate_diet(user.type_of_diet)
    translated_diet = user.type_of_diet
    meal = 'lunch'
    if request.GET == {} or request.method == 'POST':
        date_get = str(date.today())
    else:
        date_get = request.GET['date']

    http_referer = request.META.get('HTTP_REFERER', False)
    if http_referer:
        http_referer = http_referer.split('/')
        if http_referer[-2] == 'patient' and http_referer[-1] == '':
            if check_is_comment(user):
                is_have = 'comment'
    # если дата показа меньше даты госпитализации is_have = False
    if parse(date_get).date() < user.receipt_date:
        is_have = 'date'  # выводим сообщение об ошибке

    if user.type_of_diet in ['БД день 1', 'БД день 2', 'Нулевая диета']:
        is_have = 'BD'  # выводим сообщение об ошибке
        return render(request, 'patient.html', context={'is_have': is_have})

    day_of_the_week = get_day_of_the_week(date_get)

    menu_for_lk_patient = creating_menu_for_patient(date_get, diet, day_of_the_week, translated_diet)

    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))


    # queryset_main_dishes = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
    #     category='Вторые блюда').order_by(Lower('name')))
    # queryset_garnish = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
    #     category='Гарниры').order_by(Lower('name')))
    # queryset_salad = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
    #     category='Салаты').order_by(Lower('name')))
    # queryset_soup = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
    #     category='Первые блюда').order_by(Lower('name')))
    #
    # queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup = \
    #     sorting_dishes(meal, queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup)

    breakfast, afternoon, lunch, dinner = formation_menu(products)

    patient_select = create_patient_select(id, date_get)
    # patient_select = 'cafe-salad-1019'

    formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')
    date_timer = parse(date_get)
    today = (date_get == str(date.today()))
    data = {'is_have': is_have,
            'user': user,
            'breakfast': breakfast,
            'afternoon': afternoon,
            'lunch': lunch,
            'dinner': dinner,
            'date_menu': date_menu,
            'date_get': date_get,
            'date': date_timer,
            'formatted_date': formatted_date,
            'menu': menu_for_lk_patient,
            'patient_select': patient_select,
            'today': today,
            }
    # is_have = 'comment'
    # data = {'is_have': is_have}
    return render(request, 'patient.html', context=data)


def patient_history(request, id):
    # сохраняем комментарий
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        comment = CommentProduct()
        comment.user_id = user
        comment.product_id = request.POST['product_id']
        comment.comment = request.POST['text']
        comment.rating = request.POST['rating']
        comment.save()

        check_mark = '&#9989;'
        messang = f'{check_mark} <b>Отзыв на заказ от {request.POST["date"]}\n</b>'
        messang += f'{formatting_full_name(user.full_name)}\n'
        messang += f'{request.POST["product_name"]}\n'
        messang += f'Оценка {request.POST["rating"]} из 5\n'
        messang += f'{request.POST["text"]}\n'

        my_job_send_messang_changes.delay(messang)

        date_get = request.POST['date']
    # сформоровать строку с блюдами, которые пользователь уже оценил
    products_marked = []
    for item in CommentProduct.objects.filter(user_id=id):
        products_marked.append(item.product_id)
    products_marked = ' '.join(products_marked)

    if request.method == 'GET':
        if request.GET == {}:
            date_get = str(date.today())
        else:
            date_get = request.GET['date']

    day_history = date_menu_history(id, user)
    menu = creates_dict_with_menu_patients_on_day(id, date_get)
    # для тестирования меню
    # day_history = ['1']
    # menu = creates_dict_with_menu_patients_on_day(id, '2022-09-23')

    products_all = {
        'завтрак': [item for item in menu['breakfast'].values()],
        'обед': [item for item in menu['afternoon'].values()],
        'полдник': [item for item in menu['lunch'].values()],
        'ужин': [item for item in menu['dinner'].values()],
    }

    data = {'user': user,
            'day_history': day_history,
            'page': 'history',
            'date_get': date_get,
            'menu': menu,
            'products_all': products_all,
            'products_marked': products_marked
            }
    return render(request, 'patient_history.html', context=data)


def patient_history_test(request):
    return render(request, 'patient_history_test.html', {})


class SubmitPatientSelectionAPIView(APIView):
    def post(self, request):
        data = request.data

        menu = MenuByDay.objects.filter(user_id=data['id_user'])
        menu = menu.filter(date=data['date'])

        for key, value in data['menu'].items():
            main, garnish, porridge, soup, dessert, fruit, drink, salad = create_category(value)
            menu_item = menu.get(meal=key)
            menu_item.main = main
            menu_item.garnish = garnish
            menu_item.porridge = porridge
            menu_item.soup = soup
            menu_item.dessert = dessert
            menu_item.fruit = fruit
            menu_item.salad = salad
            menu_item.save()
        return Response('Ok')

def is_have_user(formatted_full_name, birthdate):
    """
    Проверяет есть ли пациент с введенными данными
    Return: Ошибка, id пациента(если такой найден)
    """
    users = CustomUser.objects.filter(full_name=formatted_full_name, status='patient')
    
    if len(users) == 0:
        return "Пользователь с такими данными не найден", None
    if len(users) > 0:
        birthdate = datetime.strptime(birthdate, '%d.%m.%Y')
        answer = []
        for user in users:
            if user.birthdate == birthdate.date():
                answer.append((None, user.id))
        if answer == []:
            return "Неверная дата рождения", None
        if len(answer) > 1:
            return f"{len(answer)} пациента с таким данными", None
        if len(answer) == 1:
            return answer[0]

def user_login(request):
    errors = None
    if request.method == 'POST':
        try:
            id = request.POST['user-id']
            user = CustomUser.objects.get(id=id)
            if user is not None:
                login(request, user)
                logging.info(f'пациент {formatting_full_name(user.full_name)} авторизовался в личном кабинете')
                return HttpResponseRedirect(reverse('patient:patient', kwargs={'id': id}))
        except:
            errors = 'Пользователя с такими данными не существует'
    return render(request, 'nutritionist/registration/login_patient.html', {'errors': errors})

def formating_name_for_login_patient(name, lastname, patronymic):
    return f'{lastname.strip().capitalize()} {name.strip().capitalize()} {patronymic.strip().capitalize()}'


class loginDataValidationAPIView(APIView):
    def post(self, request):
        data = request.data
        formatted_full_name = formating_name_for_login_patient(data['name'], data['lastname'], data['patronymic'])
        response = is_have_user(formatted_full_name, data['birthdate'])
        response = json.dumps(response)
        return Response(response)