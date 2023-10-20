from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from django.views.generic import TemplateView

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
    date_menu_history, check_is_comment, del_if_not_garnish, del_if_not_product_without_garnish
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
from scripts.statistic import get_statistic

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog-patient.log",
    format="%(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)




def group_patient_check(user):
    try:
        return user.status == 'patient'
    except:
        return False


@user_passes_test(group_patient_check, login_url='patient:patient-login')
@login_required(login_url='login')
def patient(request, id):
    is_public = True  # используем публичные названия блюд
    is_have = 'ok'
    user = CustomUser.objects.get(id=id)

    if user.type_of_diet in ['Нулевая диета'] or user.is_probe or user.is_pureed_nutrition:
        is_have = 'BD'  # выводим сообщение об ошибке
        return render(
            request,
            'patient.html',
            context={
                'is_have': is_have,
                'error_message': f'Для диеты {user.type_of_diet} выбор блюд недоступен'})

    date_menu = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + timedelta(days=2)),
    }

    if user.type_of_diet == "БД день 1":
        day_of_the_week_bd = {
            str(date.today()): "понедельник",
            str(date.today() + timedelta(days=1)): "вторник",
            str(date.today() + timedelta(days=2)): "понедельник",
        }
    if user.type_of_diet == "БД день 2":
        day_of_the_week_bd = {
            str(date.today()): "вторник",
            str(date.today() + timedelta(days=1)): "понедельник",
            str(date.today() + timedelta(days=2)): "вторник",
        }

    if request.GET == {} or request.method == 'POST':
        date_get = str(date.today())
    else:
        date_get = request.GET['date']

    diet = translate_diet(user.type_of_diet)
    translated_diet = user.type_of_diet




    if user.type_of_diet in ['БД день 1', 'БД день 2']:
        day_of_the_week = day_of_the_week_bd[date_get]
        diet = "bd"
        translated_diet = "БД"
    else:
        day_of_the_week = get_day_of_the_week(date_get)

    meal = 'lunch'

    http_referer = request.META.get('HTTP_REFERER', False)
    if http_referer:
        http_referer = http_referer.split('/')
        if http_referer[-2] == 'patient' and http_referer[-1] == '':
            if check_is_comment(user):
                is_have = 'comment'
    # если дата показа меньше даты госпитализации is_have = False
    if parse(date_get).date() < user.receipt_date:
        is_have = 'date'  # выводим сообщение об ошибке

    menu_for_lk_patient, fix_dishes = creating_menu_for_patient(date_get, diet, day_of_the_week, translated_diet, user)

    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))
    breakfast, afternoon, lunch, dinner = formation_menu(products)

    patient_select = create_patient_select(id, date_get)
    # patient_select = 'cafe-salad-1019'

    formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')
    date_timer = parse(date_get)
    today = (date_get == str(date.today()))

    # проверяем, если нет гарнира и основного блюда, тогда надо спрятать гарниры
    menu_all_lunch = MenuByDay.objects.filter(
        date=date_get, user_id=user, meal='lunch'
    ).first()
    menu_all_dinner = MenuByDay.objects.filter(
        date=date_get, user_id=user, meal='dinner'
    ).first()
    hide_side_dishes = {
        'lunch': True if getattr(menu_all_lunch, 'garnish', '') == '' and getattr(menu_all_lunch, 'main', '') == '' else False,
        'dinner': True if getattr(menu_all_dinner, 'garnish', '') == '' and getattr(menu_all_dinner, 'main', '') == '' else False,
    }
    # проверяем есть ли ганрир, если нет удаляем блюда, которые идут без гарнира
    menu_for_lk_patient = del_if_not_garnish(menu_for_lk_patient)

    # проверяем есть ли блюда в которым нужен гарнир, если нет, тогда удаляем гарниры
    # из блюд cafe
    menu_for_lk_patient = del_if_not_product_without_garnish(menu_for_lk_patient)

    # если блюдо ЛП уже с гарниром (плов)
    if user.type_of_diet not in ['БД день 1', 'БД день 2', 'Безйодовая']:
        try:
            lunch_is_with_garnish = menu_for_lk_patient['lunch']['lp']['main'][0].with_garnish
        except:
            lunch_is_with_garnish = False

        try:
            dinner_is_with_garnish = menu_for_lk_patient['dinner']['lp']['main'][0].with_garnish
        except:
            dinner_is_with_garnish = False
    else:
        lunch_is_with_garnish = dinner_is_with_garnish = False
    # fix_dishes = "lp-main-363,lp-main-465"
    fix_dishes = ','.join(fix_dishes)
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
            'lunch_is_with_garnish': lunch_is_with_garnish,
            'dinner_is_with_garnish': dinner_is_with_garnish,
            'hide_side_dishes': hide_side_dishes,
            'fix_dishes': fix_dishes,
            }
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
        'завтрак': [item for item in menu['breakfast'].values() if item not in [[None], None]],
        'обед': [item for item in menu['lunch'].values() if item not in [[None], None]],
        'полдник': [item for item in menu['afternoon'].values() if item not in [[None], None]],
        'ужин': [item for item in menu['dinner'].values() if item not in [[None], None]],
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


def patient_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('patient:patient-login'))


def patient_history_test(request):
    get_statistic()
    return render(request, 'patient_history_test.html', {})


class SubmitPatientSelectionAPIView(APIView):
    def post(self, request):
        data = request.data
        menu = MenuByDay.objects.filter(user_id=data['id_user'])
        menu = menu.filter(date=data['date'])
        patient_name = CustomUser.objects.get(id=data['id_user']).full_name

        for key, value in data['menu']['id'].items():
            category = create_category(value)
            menu_item = menu.get(meal=key)
            menu_item.main = category["main"]
            menu_item.garnish = category["garnish"]
            menu_item.porridge = category["porridge"]
            menu_item.soup = category["soup"]
            menu_item.dessert = category["dessert"]
            menu_item.fruit = category["fruit"]
            menu_item.salad = category["salad"]
            menu_item.save()

        message = f"Пациент {patient_name} ({data['id_user']}) подтвердил заказ на {data['date']}:\n"
        for meal in data['menu']['name'].keys():
            message += f"{meal}\n"
            for name in data['menu']['name'][meal]:
                message += f"   {name}\n"
        logging.info(f'{message}')
        return Response('Ok')

def is_have_user(formatted_full_name, birthdate):
    """
    Проверяет есть ли пациент с введенными данными
    Return: Ошибка, id пациента(если такой найден)
    """
    users = CustomUser.objects.filter(full_name=formatted_full_name, status='patient')
    birthdate = datetime.strptime(birthdate, '%d.%m.%Y')
    if len(users) == 0:
        error = "Пользователь с такими данными не найден"
        logging.info(f'ФИО {formatted_full_name}, дата рождения {birthdate.date()}, "{error}"')
        return error, None
    if len(users) > 0:
        answer = []
        for user in users:
            if user.birthdate == birthdate.date():
                answer.append((None, user.id))
        if answer == []:
            error = "Неверная дата рождения"
            logging.info(f'ФИО {formatted_full_name}, дата рождения {birthdate.date()}, "{error}"')
            return error, None
        if len(answer) > 1:
            error = f"{len(answer)} пациента с таким данными"
            logging.info(f'ФИО {formatted_full_name}, дата рождения {birthdate.date()}, "{error}"')
            return error, None
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
    return render(request, 'login_patient.html', {'errors': errors})

def formating_name_for_login_patient(name, lastname, patronymic):
    name = f'{lastname.strip().capitalize()} {name.strip().capitalize()} {patronymic.strip().capitalize()}'
    return name.strip()

class loginDataValidationAPIView(APIView):
    def post(self, request):
        data = request.data
        formatted_full_name = formating_name_for_login_patient(data['name'], data['lastname'], data['patronymic'])
        response = is_have_user(formatted_full_name, data['birthdate'])
        response = json.dumps(response)
        return Response(response)