from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from .forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, BotChatId, СhangesUsersToday,\
    UsersToday
from nutritionist.forms import TimetableForm
import random, calendar, datetime, logging, json
from datetime import datetime, date, timedelta
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat
from dateutil.parser import parse
from django.db.models.functions import Lower
from doctor.functions.functions import sorting_dishes, parsing, get_day_of_the_week, translate_diet, add_default_menu, \
    creates_dict_with_menu_patients, add_menu_three_days_ahead, creating_meal_menu_lp, creating_meal_menu_cafe, \
    creates_dict_with_menu_patients_on_day, delete_choices, create_user, edit_user, check_have_menu, counting_diets, \
    create_list_users_on_floor, what_meal, translate_meal, check_value_two
from doctor.functions.bot import check_change
from doctor.functions.for_print_forms import create_user_today, check_time, update_UsersToday, update_СhangesUsersToday, \
    applies_changes
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import management
import telepot


def group_doctors_check(user):
    return user.groups.filter(name='doctors').exists()


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def doctor(request):
    CustomUserFormSet = modelformset_factory(CustomUser,
                                             fields=(
                                                 'full_name', 'receipt_date', 'receipt_time', 'department',
                                                 'room_number', 'type_of_diet', 'comment', 'id'),
                                             widgets={
                                                 'full_name': TextInput(attrs={'required': "True"}),
                                                 'room_number': Select(attrs={}),
                                                 'department': Select(attrs={}),
                                                 'type_of_diet': Select(attrs={}),
                                                 'receipt_date': TextInput(),
                                                 'receipt_time': TextInput(),
                                                 'comment': Textarea(),
                                                 'id': Textarea(attrs={'style': "display: none;"}),
                                             },
                                             extra=0, )
    # create_user_today() # создаем таблицу с пользователями на сегодня
    applies_changes() # накатить изменения
    CustomUserFormSet = delete_choices(CustomUserFormSet)

    page = 'menu-doctor'
    filter_by = 'full_name'  # дефолтная фильтрация
    sorting = 'top'
    today = date.today().strftime("%d.%m.%Y")

    check_have_menu()
    add_menu_three_days_ahead()

    queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
    if request.method == 'POST' and 'filter_by_flag' in request.POST:
        filter_by = request.POST.getlist('filter_by')[0]
        if request.POST['is_pressing_again'] == 'True':
            if request.POST['sorting_value'] == 'top':
                queryset = CustomUser.objects.filter(status='patient').order_by(f'-{filter_by}')
                sorting = 'down'
            else:
                queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
                sorting = 'top'
        else:
            queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)

    if request.method == 'POST' and 'add_patient' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        # formset = \
        #     CustomUserFormSet(request.POST, request.FILES, queryset=queryset)
        create_user(user_form)
        queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
        formset = CustomUserFormSet(queryset=queryset)
        return render(request,
                      'doctor.html',
                      {'formset': formset,
                       'modal': 'patient-added',
                       'page': page,
                       'today': today,
                       'sorting': sorting,
                       'user_form': user_form,
                       'filter_by': filter_by})

    if request.method == 'POST' and 'change-email' in request.POST:
        user_form = PatientRegistrationForm()
        user = CustomUser.objects.get(id=request.user.id)
        user.email = request.POST['changed-email']
        user.username = request.POST['changed-email']
        user.save()
        formset = CustomUserFormSet(queryset=queryset)
        request.user.email = request.POST['changed-email']
        data = {
            'formset': formset,
            'page': page,
            'today': today,
            'modal': 'profile-edited',
            'sorting': sorting,
            'user_form': user_form,
            'filter_by': filter_by
        }
        return render(request, 'doctor.html', context=data)

    if request.method == 'POST' and 'change-password_flag' in request.POST:
        if request.POST['change-password_flag'] == 'on':
            user_form = PatientRegistrationForm()
            formset = CustomUserFormSet(queryset=queryset)
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(request.POST['changed-password'])
            user.save()
            data = {
                'formset': formset,
                'page': page,
                'today': today,
                'modal': 'password-edited',
                'sorting': sorting,
                'user_form': user_form,
                'filter_by': filter_by
            }
        return render(request, 'doctor.html', context=data)
    if request.method == 'POST' and 'edit_patient_flag' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        edit_user(user_form)

        formset = CustomUserFormSet(queryset=queryset)
        data = {
            'id_edited_user': user_form.data['id_edit_user'],
            'formset': formset,
            'page': page,
            'today': today,
            'sorting': sorting,
            'modal': 'edited',
            'user_form': user_form,
            'filter_by': filter_by
        }
        return render(request, 'doctor.html', context=data)

    if request.method == 'POST' and 'archive' in request.POST:
        id_user = request.POST.getlist('id_edit_user')[0]
        user = CustomUser.objects.get(id=id_user)
        user.status = 'patient_archive'
        user.save()

        if user.receipt_date <= date.today():
            if check_time():
                update_UsersToday(user)
            else:
                update_СhangesUsersToday(user)
        # applies_changes() # накатываем изменения
        if date.today() >= user.receipt_date:
            snowflake = u'\u2757\ufe0f'  # Code: 600's snowflake
            TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
            bot = telepot.Bot(TOKEN)
            # все номера chat_id
            messang = ''
            messang += f'{snowflake} Изменение с {check_change(user)}\n'
            messang += f'Пациента {user.full_name} выписали.\n'
            for item in BotChatId.objects.all():
                bot.sendMessage(item.chat_id, messang)

        user_form = PatientRegistrationForm(request.POST)
        formset = CustomUserFormSet(queryset=queryset)
        if not formset.is_valid():
            data = {
                'modal': 'archived',
                'formset': formset,
                'page': page,
                'today': today,
                'sorting': sorting,
                'user_form': user_form,
                'filter_by': filter_by
            }
            return render(request, 'doctor.html', context=data)
        else:
            formset.save()
            queryset = CustomUser.objects.filter(status='patient')
            formset = CustomUserFormSet(queryset=queryset)
            data = {
                'modal': 'archive',
                'page': page,
                'today': today,
                'formset': formset,
                'sorting': sorting,
                'user_form': user_form,
                'filter_by': filter_by
            }
        return render(request, 'doctor.html', context=data)
    user_form = PatientRegistrationForm()
    formset = CustomUserFormSet(queryset=queryset)
    data = {
        # 'menu_patients': menu_patients,
        'formset': formset,
        'page': page,
        'today': today,
        'sorting': sorting,
        'user_form': user_form,
        'filter_by': filter_by
    }
    return render(request, 'doctor.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def archive(request):
    CustomUserFormSet = modelformset_factory(CustomUser,
                                             fields=(
                                                 'full_name', 'receipt_date', 'receipt_time', 'department',
                                                 'room_number', 'type_of_diet', 'comment', 'id'),
                                             widgets={
                                                 'full_name': TextInput(attrs={'class': 'form-control'}),
                                                 'room_number': Select(attrs={'class': 'form-control'}),
                                                 'department': Select(attrs={'class': 'form-control'}),
                                                 'type_of_diet': Select(attrs={'class': 'form-control'}),
                                                 'receipt_date': DateInput(format='%Y-%m-%d',
                                                                           attrs={'class': 'form-control',
                                                                                  'type': 'date'}),
                                                 'receipt_time': TimeInput(
                                                     attrs={'class': 'form-control', 'type': 'time'}),
                                                 'comment': TextInput(
                                                     attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),
                                                 'id': Textarea(attrs={'style': "display: none;"}),
                                             },
                                             extra=0, )

    page = 'menu-archive'
    filter_by = 'full_name'  # дефолтная фильтрация
    sorting = 'top'

    queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
    if request.method == 'POST' and 'filter_by_flag' in request.POST:
        filter_by = request.POST.getlist('filter_by')[0]
        if request.POST['is_pressing_again'] == 'True':
            if request.POST['sorting_value'] == 'top':
                queryset = CustomUser.objects.filter(status='patient_archive').order_by(f'-{filter_by}')
                sorting = 'down'
            else:
                queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
                sorting = 'top'
        else:
            queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)

    if request.method == 'POST' and 'change-email' in request.POST:
        # сhange_password(request.POST['changed-email'], request)
        user_form = PatientRegistrationForm()
        user = CustomUser.objects.get(id=request.user.id)
        user.email = request.POST['changed-email']
        user.username = request.POST['changed-email']
        user.save()
        formset = CustomUserFormSet(queryset=queryset)
        request.user.email = request.POST['changed-email']
        data = {
            'formset': formset,
            'page': page,
            'modal': 'profile-edited',
            'sorting': sorting,
            'user_form': user_form,
            'filter_by': filter_by
        }
        return render(request, 'doctor.html', context=data)

    if request.method == 'POST' and 'change-password_flag' in request.POST:
        if request.POST['change-password_flag'] == 'on':
            user_form = PatientRegistrationForm()
            formset = CustomUserFormSet(queryset=queryset)
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(request.POST['changed-password'])
            user.save()
            data = {
                'formset': formset,
                'page': page,
                'modal': 'password-edited',
                'sorting': sorting,
                'user_form': user_form,
                'filter_by': filter_by
            }
            return render(request, 'doctor.html', context=data)

    if request.method == 'POST' and 'archive' in request.POST:
        id_user = request.POST.getlist('id_edit_user')[0]
        user = CustomUser.objects.get(id=id_user)
        user.status = 'patient'
        user.save()
        user_form = PatientRegistrationForm(request.POST)
        formset = \
            CustomUserFormSet(queryset=queryset)
        if not formset.is_valid():
            data = {
                'sorting': sorting,
                'formset': formset,
                'page': page,
                'modal': 'patient-restored',
                'user_form': user_form,
                'filter_by': filter_by,
            }
            return render(request, 'archive.html', context=data)
        else:
            formset.save()
            queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
            formset = CustomUserFormSet(queryset=queryset)
            data = {
                'sorting': sorting,
                'formset': formset,
                'user_form': user_form,
                'page': page,
                'modal': 'patient-restored',
                'filter_by': filter_by,
            }
        return render(request, 'archive.html', context=data)

    user_form = PatientRegistrationForm()
    formset = CustomUserFormSet(queryset=queryset)
    data = {
        'sorting': sorting,
        'formset': formset,
        'user_form': user_form,
        'page': page,
        'filter_by': filter_by,
    }
    return render(request, 'archive.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def menu(request):
    import datetime
    page = 'menu-menu'
    date_menu = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + datetime.timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + datetime.timedelta(days=2)),
    }

    if request.GET == {} or request.method == 'POST':
        diet_form = DietChoiceForm({'type_of_diet': 'ovd'})
        diet = 'ovd'
        date_get = str(date.today())

        meal = 'breakfast'

    else:
        diet = request.GET['input_type_of_diet']
        date_get = request.GET['date']

        diet_form = DietChoiceForm(request.GET)
        meal = request.GET['meal']
    day_of_the_week = get_day_of_the_week(date_get)
    translated_diet = translate_diet(diet)

    products_lp: tuple = creating_meal_menu_lp(day_of_the_week, translated_diet, meal)

    products_main, products_garnish, products_salad, \
    products_soup, products_porridge, products_dessert, \
    products_fruit, products_drink = products_lp

    products_cafe: tuple = creating_meal_menu_cafe(date_get, diet, meal)

    queryset_main_dishes, queryset_garnish, queryset_salad, \
    queryset_soup = products_cafe

    formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')

    if request.method == 'POST' and 'change-email' in request.POST:
        # сhange_password(request.POST['changed-email'], request)

        user = CustomUser.objects.get(id=request.user.id)
        user.email = request.POST['changed-email']
        user.username = request.POST['changed-email']
        user.save()
        request.user.email = request.POST['changed-email']
        data = {
            'diet_form': diet_form,
            'date_menu': date_menu,
            'products_main': products_main + queryset_main_dishes,
            'products_porridge': products_porridge,
            'products_dessert': products_dessert,
            'products_fruit': products_fruit,
            'products_garnish': products_garnish + queryset_garnish,
            'products_salad': products_salad + queryset_salad,
            'products_soup': products_soup + queryset_soup,
            'products_drink': products_drink,
            'page': page,
            'date_get': date_get,
            'formatted_date': formatted_date,
            'meal': meal,
            'modal': 'profile-edited',

        }
        return render(request, 'menu.html', context=data)

    if request.method == 'POST' and 'changed-password' in request.POST:
        user = CustomUser.objects.get(id=request.user.id)
        user.set_password(request.POST['changed-password'])
        user.save()
        data = {
            'diet_form': diet_form,
            'date_menu': date_menu,
            'products_main': products_main + queryset_main_dishes,
            'products_porridge': products_porridge,
            'products_dessert': products_dessert,
            'products_fruit': products_fruit,
            'products_garnish': products_garnish + queryset_garnish,
            'products_salad': products_salad + queryset_salad,
            'products_soup': products_soup + queryset_soup,
            'products_drink': products_drink,
            'page': page,
            'date_get': date_get,
            'formatted_date': formatted_date,
            'meal': meal,
            'modal': 'password-edited',

        }
        return render(request, 'menu.html', context=data)

    data = {'diet_form': diet_form,
            'date_menu': date_menu,
            'products_main': products_main + queryset_main_dishes,
            'products_porridge': products_porridge,
            'products_dessert': products_dessert,
            'products_fruit': products_fruit,
            'products_garnish': products_garnish + queryset_garnish,
            'products_salad': products_salad + queryset_salad,
            'products_soup': products_soup + queryset_soup,
            'products_drink': products_drink,
            'page': page,
            'date_get': date_get,
            'formatted_date': formatted_date,
            'meal': meal,
            'diet': diet,
            }
    return render(request, 'menu.html', context=data)


def printed_form_one(request):
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = str(datetime.today().time().hour) + ':' + str(datetime.today().time().minute)
    # какой прием пищи
    meal = what_meal()
    users = UsersToday.objects.all()
    users = users.filter(status='patient').filter(receipt_date__lte=date.today())
    catalog = {'meal': translate_meal(meal),
               'count': len(users),
               'count_diet': counting_diets(users),
               'users_2nd_floor': create_list_users_on_floor(users, 200, 299, meal),
               'users_3nd_floor': create_list_users_on_floor(users, 300, 399, meal)
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

    data = {
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'count_users_with_cafe_prod': count_users_with_cafe_prod
    }
    return render(request, 'printed_form1.html', context=data)


def printed_form_two_lp(request):
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = str(datetime.today().time().hour) + ':' + str(datetime.today().time().minute)
    # какой прием пищи
    # meal = what_meal()
    meal = 'lunch'
    catalog = {}

    users = CustomUser.objects.all()
    users = users.filter(status='patient').filter(receipt_date__lte=date.today())
    for category in ['main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit', 'drink', 'salad']:
        list_whith_unique_products = []
        for diet in ['ОВД', 'ОВД без сахара', 'ЩД', 'БД', 'ВБД', 'НБД', 'НКД', 'ВКД']:
            users_with_diet = users.filter(type_of_diet=diet)
            all_products = []
            for user in users_with_diet:
                menu_all = MenuByDay.objects.filter(user_id=user.id)
                all_products.append(check_value_two(menu_all, str(date.today()), meal, category))
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
                un_product['count'] = str(count)
                un_product['diet'] = diet
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
                        cat[ii] = None

    data = {
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'meal': translate_meal(meal)
    }
    return render(request, 'printed_form2_lp.html', context=data)


def printed_form_two_cafe(request):
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = str(datetime.today().time().hour) + ':' + str(datetime.today().time().minute)
    # какой прием пищи
    # meal = what_meal()
    meal = 'lunch'
    catalog = {}

    users = CustomUser.objects.all()
    users = users.filter(status='patient').filter(receipt_date__lte=date.today())
    for category in ['main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit', 'drink', 'salad']:
        list_whith_unique_products = []
        for diet in ['ОВД', 'ОВД без сахара', 'ЩД', 'БД', 'ВБД', 'НБД', 'НКД', 'ВКД']:
            users_with_diet = users.filter(type_of_diet=diet)
            all_products = []
            for user in users_with_diet:
                menu_all = MenuByDay.objects.filter(user_id=user.id)
                all_products.append(check_value_two(menu_all, str(date.today()), meal, category))
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
                        if 'cafe' in product['id']:
                            unique_products.append(product)
            # добавляем элеметны списока с уникальными продуктами, кол-вом(сколько продуктов всего)
            # типом диеты
            for un_product in unique_products:
                count = 0
                for product in all_products:
                    if product['id'] == un_product['id']:
                        count += 1
                un_product['count'] = str(count)
                un_product['diet'] = diet
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
                        cat[ii] = None

    data = {
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'catalog': catalog,
        'meal': translate_meal(meal)
    }
    return render(request, 'printed_form2_cafe.html', context=data)


def admin(request):
    data = {}
    return render(request, 'admin.html', context=data)


class VerifyPasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        user = CustomUser.objects.get(id=data['id_user'])
        row_password = data['row_password']
        if user.check_password(row_password):
            return Response('Yes')
        else:
            return Response('No')


class GetPatientMenuAPIView(APIView):
    def post(self, request):
        data = request.data
        response = creates_dict_with_menu_patients(data['id_user'])
        response = json.dumps(response)
        return Response(response)


class GetPatientMenuDayAPIView(APIView):
    def post(self, request):
        data = request.data
        response = creates_dict_with_menu_patients_on_day(data['id_user'], data['date_show'])
        response = json.dumps(response)
        return Response(response)


def test(request):
    data = {}
    return render(request, 'test.html', context=data)
