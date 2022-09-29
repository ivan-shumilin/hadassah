from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from doctor.forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, CommentProduct, BotChatId
from nutritionist.forms import TimetableForm
import random, calendar, datetime
from datetime import datetime, date, timedelta
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat
from dateutil.parser import parse
from django.db.models.functions import Lower
from doctor.functions import sorting_dishes, parsing, get_day_of_the_week, translate_diet, creating_meal_menu_cafe,\
    creating_meal_menu_lp, creates_dict_with_menu_patients_on_day
from patient.functions import formation_menu, creating_menu_for_lk_patient, create_category, create_patient_select,\
    date_menu_history
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
import telepot


def group_patient_check(user):
    return user.groups.filter(name='patients').exists()


# @login_required
# @user_passes_test(group_patient_check, login_url='login')
def patient(request, id):
    import datetime
    page = 'menu-menu'
    date_menu = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + datetime.timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + datetime.timedelta(days=2)),
    }


    user = CustomUser.objects.get(id=id)
    diet = translate_diet(user.type_of_diet)
    translated_diet = user.type_of_diet
    meal = 'lunch'
    if request.GET == {} or request.method == 'POST':
        date_get = str(date.today())

    else:
        date_get = request.GET['date']

    # если дата показа меньше даты госпитализации is_have = false
    is_have = parse(date_get).date() >= user.receipt_date

    day_of_the_week = get_day_of_the_week(date_get)

    menu_for_lk_patient = creating_menu_for_lk_patient(date_get, diet, meal, day_of_the_week, translated_diet)


    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))


    queryset_main_dishes = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Вторые блюда').order_by(Lower('name')))
    queryset_garnish = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Гарниры').order_by(Lower('name')))
    queryset_salad = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Салаты').order_by(Lower('name')))
    queryset_soup = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Первые блюда').order_by(Lower('name')))

    queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup = \
        sorting_dishes(meal, queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup)

    breakfast, afternoon, lunch, dinner = formation_menu(products)

    patient_select = create_patient_select(id, date_get)
    # patient_select = 'cafe-salad-1162,cafe-soup-1161,cafe-main-1094'


    formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')
    date_timer = parse(date_get)
    data = {'is_have': is_have,
            'user': user,
            'breakfast': breakfast,
            'afternoon': afternoon,
            'lunch': lunch,
            'dinner': dinner,
            'date_menu': date_menu,
            'page': page,
            'date_get': date_get,
            'date': date_timer,
            'formatted_date': formatted_date,
            'products': menu_for_lk_patient,
            'patient_select': patient_select
            }
    return render(request, 'patient_.html', context=data)


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

        TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
        bot = telepot.Bot(TOKEN)
        # все номера chat_id
        messang = ''
        messang += f'Отзыв на заказ от {request.POST["date"]}\n'
        messang += f'{user.full_name}\n'
        messang += f'{request.POST["product_name"]}\n'
        messang += f'{request.POST["rating"]}/5\n'
        messang += f'{request.POST["text"]}\n'
        for item in BotChatId.objects.all():
            bot.sendMessage(item.chat_id, messang)

    # сформоровать строку с блюдами, которые пользователь уже оценил
    products_marked = []
    for item in CommentProduct.objects.filter(user_id=id):
        products_marked.append(item.product_id)
    products_marked = ' '.join(products_marked)

    if request.GET == {} or request.method == 'POST':
        date_get = str(date.today())

    else:
        date_get = request.GET['date']
    day_history = date_menu_history(id, user)
    menu = creates_dict_with_menu_patients_on_day(id, date_get)
    # для тестирования меню
    # day_history = ['1']
    # menu = creates_dict_with_menu_patients_on_day(id, '2022-09-23')

    breakfast = []
    afternoon = []
    lunch = []
    dinner = []

    [breakfast.append(item) for item in menu['breakfast'].values()]
    [afternoon.append(item) for item in menu['afternoon'].values()]
    [lunch.append(item) for item in menu['lunch'].values()]
    [dinner.append(item) for item in menu['dinner'].values()]
    data = {'user': user,
            'day_history': day_history,
            'page': 'history',
            'date_get': date_get,
            'menu': menu,
            'breakfast': breakfast,
            'afternoon': afternoon,
            'lunch': lunch,
            'dinner': dinner,
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
            menu_item.drink = drink
            menu_item.salad = salad
            menu_item.save()




        return Response('Ok')

