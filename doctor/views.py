from collections import OrderedDict

from PIL import Image
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput, CheckboxInput
from drf_spectacular.utils import extend_schema_view, extend_schema

from .forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, BotChatId, СhangesUsersToday, \
    UsersToday, TimetableLp, Ingredient, MenuByDayReadyOrder, UsersReadyOrder, ModifiedDish
from nutritionist.forms import TimetableForm
import random, calendar, datetime, logging, json
from datetime import datetime, date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat
from django.contrib import messages
from django.contrib.messages import get_messages
from dateutil.parser import parse
from django.db.models.functions import Lower
from doctor.functions.functions import sorting_dishes, parsing, \
    creates_dict_with_menu_patients, creating_meal_menu_lp, creating_meal_menu_cafe, \
    creates_dict_with_menu_patients_on_day, delete_choices, create_user, edit_user, counting_diets, \
    create_list_users_on_floor, what_meal, translate_meal, check_value_two, archiving_user, get_not_active_users_set, \
    get_occupied_rooms, creates_dict_with_menu_patients_on_day_test, what_type_order, get_order_status
from doctor.functions.bot import check_change, do_messang_send, formatting_full_name
from doctor.functions.for_print_forms import create_user_today, check_time, update_UsersToday, update_СhangesUsersToday, \
    applies_changes, create_user_tomorrow, create_ready_order, create_report, create_products_lp, add_products_lp,\
    add_products_lp, create_product_storage
from doctor.functions.diet_formation import add_menu_three_days_ahead, update_diet_bd
from doctor.functions.translator import get_day_of_the_week, translate_diet
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import management
import telepot
from doctor.tasks import send_messang, my_job_create_ready_order_dinner
from .functions.download import get_token, download
from .logic.create_ingredient import create_ingredients


from django.shortcuts import render
from django.views.generic import TemplateView

from .serializer import DishesSerializer, PatientsSerializer, InfoPatientSerializer, InputDataSerializer, \
    AddDishSerializer, ChangeDishSerializer, CroppImageSerializer


class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'


@transaction.atomic
def load_nomenclature():
    with open("nomenclature.json", "r") as my_file:
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




def group_doctors_check(user):
    return user.groups.filter(name='doctors').exists()
def group_doctors_check_guest(user):
    return user.groups.filter(name='guest').exists() or user.groups.filter(name='doctors').exists()


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def doctor(request):
    CustomUserFormSet = modelformset_factory(CustomUser,
                                             fields=(
                                                 'full_name', 'birthdate', 'receipt_date', 'receipt_time', 'department',
                                                 'floor', 'room_number', 'bed', 'type_of_diet', 'comment', 'id',
                                                 'is_accompanying', 'is_probe', 'is_without_salt',
                                                 'is_pureed_nutrition', 'is_without_lactose', 'type_pay', 'extra_bouillon'),
                                             widgets={
                                                 'full_name': TextInput(attrs={'required': "True"}),
                                                 'birthdate': TextInput(),
                                                 'room_number': Select(attrs={}),
                                                 'floor': TextInput(),
                                                 'bed': Select(attrs={}),
                                                 'department': Select(attrs={}),
                                                 'type_of_diet': Select(attrs={}),
                                                 'receipt_date': TextInput(),
                                                 'receipt_time': TextInput(),
                                                 'comment': Textarea(),
                                                 'id': Textarea(attrs={'style': "display: none;"}),
                                                 'is_accompanying': TextInput(attrs={'required': "True"}),
                                                 'type_pay': TextInput(attrs={'required': "True"}),
                                                 'is_probe': TextInput(attrs={'required': "True"}),
                                                 'is_without_salt': TextInput(attrs={'required': "True"}),
                                                 'is_pureed_nutrition': TextInput(attrs={'required': "True"}),
                                                 'is_without_lactose': TextInput(attrs={'required': "True"}),
                                                 'extra_bouillon': TextInput(attrs={'required': "True"}),
                                             },
                                             extra=0,)

    # load_nomenclature()
    # load_ttk()
    # create_ingredients()
    # get_token()


    not_active_users_set = get_not_active_users_set()

    CustomUserFormSet = delete_choices(CustomUserFormSet)

    page = 'menu-doctor'
    filter_by = 'full_name'  # дефолтная фильтрация
    sorting = 'top'
    today = date.today().strftime("%d.%m.%Y")



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
        create_user(user_form, request)
        messages.add_message(request, messages.INFO, 'patient-added')
        return HttpResponseRedirect(reverse('doctor'))

    if request.method == 'POST' and 'edit_patient_flag' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        is_edited = edit_user(user_form, 'edit', request)
        if is_edited:
            messages.add_message(request, messages.INFO, 'edited')
        else:
            messages.add_message(request, messages.INFO, 'patient was discharged')
        return HttpResponseRedirect(reverse('doctor'))

    if request.method == 'POST' and 'archive' in request.POST:
        id_user = request.POST.getlist('id_edit_user')[0]
        user = CustomUser.objects.get(id=id_user)
        modal = archiving_user(user, request)
        messages.add_message(request, messages.INFO, modal)
        return HttpResponseRedirect(reverse('doctor'))

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
            'filter_by': filter_by,
            'not_active_users_set': not_active_users_set
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
                ' ': 'password-edited',
                'sorting': sorting,
                'user_form': user_form,
                'filter_by': filter_by,
                'not_active_users_set': not_active_users_set
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
        'filter_by': filter_by,
        'not_active_users_set': not_active_users_set
    }
    return render(request, 'doctor.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def archive(request):
    CustomUserFormSet = modelformset_factory(CustomUser,
                                             fields=(
                                                 'full_name','birthdate', 'receipt_date', 'receipt_time', 'department',
                                                 'floor', 'room_number', 'bed', 'type_of_diet', 'comment', 'id'),
                                             widgets={
                                                 'full_name': TextInput(attrs={'class': 'form-control'}),
                                                 'birthdate': DateInput(format='%Y-%m-%d',
                                                                           attrs={'class': 'form-control',
                                                                                  'type': 'date'}),
                                                 'room_number': Select(attrs={'class': 'form-control'}),
                                                 'bed': Select(attrs={'class': 'form-control'}),
                                                 'department': Select(attrs={'class': 'form-control'}),
                                                 'floor': TextInput(attrs={'class': 'form-control'}),
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

    CustomUserFormSet = delete_choices(CustomUserFormSet)
    page = 'menu-archive'
    filter_by = 'full_name'  # дефолтная фильтрация
    sorting = 'top'
    queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
    # full_name__icontains = "Алекс"
    # если есть поисковый запрос, то фильтруем по нему
    count: int = 100
    search_query_filter: Q = Q()
    try:
        search_query = request.POST.getlist('search')[0]
        search_query_filter = Q(full_name__icontains=search_query)
        count: int = 150
    except:
        pass
    queryset = queryset.filter(search_query_filter)

    if request.method == 'POST' and 'filter_by_flag' in request.POST:
        filter_by = request.POST.getlist('filter_by')[0]
        if request.POST['is_pressing_again'] == 'True':
            if request.POST['sorting_value'] == 'top':
                queryset = queryset.order_by(f'-{filter_by}')
                sorting = 'down'
            else:
                queryset = queryset.order_by(filter_by)
                sorting = 'top'


    if request.method == 'POST' and 'archive' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        is_archive = edit_user(user_form, 'restore', request)
        if is_archive:
            messages.add_message(request, messages.INFO, 'patient-restored')
        return HttpResponseRedirect(reverse('archive'))

    if request.method == 'POST' and 'change-email' in request.POST:
        # сhange_password(request.POST['changed-email'], request)
        user_form = PatientRegistrationForm()
        user = CustomUser.objects.get(id=request.user.id)
        user.email = request.POST['changed-email']
        user.username = request.POST['changed-email']
        user.save()
        formset = CustomUserFormSet(queryset=queryset.all()[:count])
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
            formset = CustomUserFormSet(queryset=queryset.all()[:count])
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

    user_form = PatientRegistrationForm()
    formset = CustomUserFormSet(queryset=queryset.all()[:count])
    data = {
        'sorting': sorting,
        'formset': formset,
        'user_form': user_form,
        'page': page,
        'filter_by': filter_by,
    }
    return render(request, 'archive.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_doctors_check_guest, login_url='login')
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

    if diet == 'БД':
        if date_get == date_menu['today']:
            day_of_the_week = 'понедельник'
        else:
            day_of_the_week = 'вторник'
            date_get = date_menu['tomorrow']
    else:
        day_of_the_week = get_day_of_the_week(date_get)

    translated_diet = translate_diet(diet)

    products_lp: tuple = creating_meal_menu_lp(day_of_the_week, translated_diet, meal)

    products_main, products_garnish, products_salad, \
    products_soup, products_porridge, products_dessert, \
    products_fruit, products_drink = products_lp

    if diet not in ['ОВД веган (пост) без глютена', 'Нулевая диета', 'БД', 'Безйодовая', 'ПЭТ/КТ']:
        products_cafe: tuple = creating_meal_menu_cafe(date_get, diet, meal)
    else:
        products_cafe: tuple = ([], [], [], [], [], [])
    queryset_main_dishes, queryset_garnish, queryset_salad, \
    queryset_soup, queryset_breakfast, queryset_porridge = products_cafe

    formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')

    if meal == 'breakfast':
        products_main += queryset_breakfast
    else:
        products_main += queryset_main_dishes



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
            'products_main': products_main,
            'products_porridge': products_porridge + queryset_porridge,
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
            'products_main': products_main,
            'products_porridge': products_porridge + queryset_porridge,
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
            'products_main': products_main,
            'products_porridge': products_porridge + queryset_porridge,
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
    """Возвращает выбранные блюда пациента. ЛК врача, карточка пациента."""
    def post(self, request):
        data = request.data
        response = creates_dict_with_menu_patients(data['id_user'])
        response = json.dumps(response)
        return Response(response)


class GetOccupiedRoomsAPIView(APIView):
    def post(self, request):
        user_script = request.data
        response = get_occupied_rooms(user_script['user_script'])
        response = json.dumps(response)
        return Response(response)


class GetPatientMenuDayAPIView(APIView):
    def post(self, request):
        data = request.data
        response = creates_dict_with_menu_patients_on_day(data['id_user'], data['date_show'])
        response = json.dumps(response)
        return Response(response)


# Пока скопировал ручку GetPatientMenuDayAPIView, проверю работу и верну.
# class GetPatientMenuDayTestAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         response = creates_dict_with_menu_patients_on_day_test(data['id_user'], data['date_show'])
#         response = json.dumps(response)
#         return Response(response)

class GetPatientMenuDayTestAPIView(APIView):
    def post(self, request):
        serializer = InputDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_user = serializer.validated_data['id_user']
        date_show = serializer.validated_data['date_show']
        response = creates_dict_with_menu_patients_on_day_test(id_user, date_show)
        response = json.dumps(response)
        return Response(response)


def get_day_of_the_week(date):
    number_day_of_the_week = {
    '1': 'понедельник',
    '2': 'вторник',
    '3': 'среда',
    '4': 'четверг',
    '5': 'пятница',
    '6': 'суббота',
    '7': 'воскресенье',
    }
    date = datetime.strptime(date, '%Y-%m-%d')
    return number_day_of_the_week[str(date.isoweekday())]

def get_category(category):
    categorys = {
        'salad': ["салат"],
        'soup': ["суп"],
        'porridge': ["каша"],
        'main': ["основной"],
        'garnish': ["гарнир"],
        'dessert': ["десерт"],
        'fruit': ["фрукты"],
        'drink': ["напиток"],
        'products': ["товар", "hidden"],
        'hidden': ["hidden"],
        'bouillon': ["бульон"],
    }
    return categorys[category]

def get_category_cafe(category):
    categorys = {
        "салат": ["Салаты"],
        "суп": ["Первые блюда"],
        "каша": ["Каши"],
        "основной": ["Завтраки", "Вторые блюда", "Блюда от шефа"],
        "гарнир": ["Гарниры"]
    }
    return categorys.get(category[0], [])


class GetPatientsAPIView(APIView):
    def get(self, request):
        date = request.GET['date']
        sort_field = request.GET['filter']

        patients = CustomUser.objects.filter(status='patient').order_by(sort_field)
        serializer = PatientsSerializer(patients, many=True)
        return Response(serializer.data)


class GetInfoPatientAPIView(APIView):
    def get(self, request):
        user_id = request.GET['user_id']

        try:
            patient = CustomUser.objects.get(id=user_id)
        except:
            return Response({'status': 'Error'})

        serializer = InfoPatientSerializer(patient)
        return Response(serializer.data)

class GetAllDishesByCategoryAPIView(APIView):
    def get(self, request):
        all_diet = {
            'ОВД',
            'ОВД без сахара',
            'ОВД веган (пост) без глютена',
            'Нулевая диета',
            'ЩД',
            'ЩД без сахара',
            'БД',
            'БД день 1',
            'БД день 2',
            'НБД',
            'ВБД',
            'НКД',
            'ВКД',
            'Безйодовая',
            'ВКД',
            'ПЭТ/КТ',
            'Без ограничений'
        }
        category = request.GET['category']
        date = request.GET['date']
        meal = request.GET['meal']
        day_of_the_week = get_day_of_the_week(date)
        category = get_category(category)
        # Активные приемы пищи
        active_diet = MenuByDay.objects.filter(date=date, meal=meal).values_list('type_of_diet', flat=True).distinct()

        # Другие приемы пищи по другим активным диетам
        dishes_all = TimetableLp.objects.filter(day_of_the_week=day_of_the_week,
                                            item__category__in=category,
                                            type_of_diet__in=active_diet
                                            ).distinct('item__name')

        # Аналогичный прием пищи по другим активным диетам
        dishes_meal = dishes_all.filter(meals=meal)

        # Блюда линни раздачи
        dishes_cafe = Timetable.objects.filter(datetime=date,
                                            item__category__in=get_category_cafe(category),
                                            ).distinct('item__name')

        # Аналогичный прием пищи по неактивным диетам
        no_active_diet = all_diet - set(active_diet)
        dishes_no_active_diet = TimetableLp.objects.filter(day_of_the_week=day_of_the_week,
                                                           item__category__in=category,
                                                           type_of_diet__in=no_active_diet,
                                                           meals=meal
                                                           ).distinct('item__name')

        dishes_all = DishesSerializer(dishes_all, many=True, context={'type': 'lp'}).data
        dishes_meal = DishesSerializer(dishes_meal, many=True, context={'type': 'lp'}).data
        dishes_cafe = DishesSerializer(dishes_cafe, many=True, context={'type': 'cafe'}).data
        dishes_no_active_diet = DishesSerializer(dishes_no_active_diet, many=True, context={'type': 'lp'}).data
        other = [
            OrderedDict([
                ('name', 'Сыр Гауда 60 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 482),
                ('description', 'Сыр Гауда.')
            ])
        ]
        data ={
            "dishes_all": dishes_all,
            "dishes_meal": dishes_meal,
            "dishes_cafe": dishes_cafe,
            "dishes_no_active_diet": dishes_no_active_diet,
            "other": other
        }
        return Response(data)


class DeleteDishAPIView(APIView):
    def delete(self, request):
        serializer = AddDishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_user: str = serializer.validated_data['id_user']
        date = serializer.validated_data['date']
        product_id: str = serializer.validated_data['product_id']
        category: str = serializer.validated_data['category']
        meal: str = serializer.validated_data['meal']

        changes: list = []  # список с меню в который надо внести изменения

        # Проверка времани, если заказ уже сформирован (менее 2х часов до приема пищи)
        # вносить изменения в MenuByDayReadyOrder
        order_status: str = get_order_status(meal, date)
        menu = MenuByDay.objects.all()
        changes.append((menu, id_user))
        if order_status == 'fix-order':
            menu = MenuByDayReadyOrder.objects.all()
            patient = UsersReadyOrder.objects.filter(user_id=id_user).first()
            changes.append((menu, patient))
        with transaction.atomic():
            for menu, id in changes:
                try:
                    item_menu = menu.get(user_id=id, date=date, meal=meal)
                except:
                    return Response({'status': 'Error'})
    
                products = getattr(item_menu, category)
                products = products.split(',')
                products.remove(product_id)
                products = ','.join(products)
                setattr(item_menu, category, products)
                item_menu.save()
            
            # удалить из ModifiedDish если есть
            patient = CustomUser.objects.filter(id=id_user).first()
            try:
                ModifiedDish.objects\
                    .filter(product_id=product_id, date=date, meal=meal, user_id=patient).first().delete()
            except:
                pass

            return Response({'status':'OK'})


class AddDishAPIView(APIView):
    def post(self, request):
        serializer = AddDishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_user: str = serializer.validated_data['id_user']
        date = serializer.validated_data['date']
        product_id: str = serializer.validated_data['product_id']
        category: str = serializer.validated_data['category']
        meal: str = serializer.validated_data['meal']

        changes: list = []  # список с меню в который надо внести изменения

        # Проверка времани, если заказ уже сформирован (менее 2х часов до приема пищи)
        # вносить изменения в MenuByDayReadyOrder
        # type_order = what_type_order()
        order_status: str = get_order_status(meal, date)
        menu = MenuByDay.objects.all()
        changes.append((menu, id_user))
        if order_status == 'fix-order':
            menu = MenuByDayReadyOrder.objects.all()
            patient = UsersReadyOrder.objects.filter(user_id=id_user).first()
            changes.append((menu, patient))
        with transaction.atomic():
            for menu, id in changes:
                try:
                    item_menu = menu.get(user_id=id, date=date, meal=meal)
                except:
                    return Response({'status': 'Error'})

                products = getattr(item_menu, category)
                if products == "":
                    products = product_id
                else:
                    products = products.split(',')
                    products.append(product_id)
                    products = ','.join(products)
                setattr(item_menu, category, products)
                item_menu.save()
            # добавить изменения в ModifiedDish
            user = CustomUser.objects.get(id=id_user)
            ModifiedDish(product_id=product_id, date=date, meal=meal, user_id=user, status="add").save()

        return Response({'status':'OK'})


class ChangeDishAPIView(APIView):
    def put(self, request):
        serializer = ChangeDishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_user: str = serializer.validated_data['id_user']
        date = serializer.validated_data['date']
        category: str = serializer.validated_data['category']
        meal: str = serializer.validated_data['meal']
        product_id_add: str = serializer.validated_data['product_id_add']
        product_id_del: str = serializer.validated_data['product_id_del']
        changes: list = []  # список с меню в который надо внести изменения

        # Проверка времани, если заказ уже сформирован (менее 2х часов до приема пищи)
        # вносить изменения в MenuByDayReadyOrder
        order_status: str = get_order_status(meal, date)
        menu = MenuByDay.objects.all()
        changes.append((menu, id_user))
        if order_status == 'fix-order':
            menu = MenuByDayReadyOrder.objects.all()
            patient = UsersReadyOrder.objects.filter(user_id=id_user).first()
            changes.append((menu, patient))
        with transaction.atomic():
            for menu, id in changes:
                try:
                    with transaction.atomic():
                        item_menu = menu.select_for_update().get(user_id=id, date=date, meal=meal)
                        products = getattr(item_menu, category)
                        products = products.split(',')
                        products.remove(product_id_del)
                        products = ','.join(products)
                        setattr(item_menu, category, products)

                        products = getattr(item_menu, category)
                        if products == "":
                            products = product_id_add
                        else:
                            products = products.split(',')
                            products.append(product_id_add)
                            products = ','.join(products)
                        setattr(item_menu, category, products)
                        item_menu.save()

                except:
                    return Response({'status': 'Error'})
            # удалить из ModifiedDish если есть
            patient = CustomUser.objects.filter(id=id_user).first()
            try:
                ModifiedDish.objects\
                    .filter(product_id=product_id_del, date=date, meal=meal, user_id=patient).first().delete()
            except:
                pass
            # добавить изменения в ModifiedDish
            user = CustomUser.objects.get(id=id_user)
            ModifiedDish(product_id=product_id_add, date=date, meal=meal, user_id=user, status="change").save()
        return Response({'status': 'OK'})


class CroppImageAPIView(APIView):
    def post(self, request):
        QUALITY = {
            'full': 75,
            'min': 30
        }

        serializer = CroppImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        x: int = serializer.validated_data['x']
        y: int = serializer.validated_data['y']
        width: int = serializer.validated_data['width']
        height: int = serializer.validated_data['height']
        url: str = '.' + serializer.validated_data['url']
        type: str = serializer.validated_data['type']

        im = Image.open(url)
        im_crop = im.crop((x, y, x + width, y + height))
        im_crop.save(url, quality=QUALITY.get(type, 75))
        Response({'status': 'OK'})

        return Response({'status': 'OK'})


# def menu_for_staff(request):
#     type = 'menu_for_staff'
#     import datetime
#
#     page = 'menu-menu'
#     date_menu = {
#         'today': str(date.today()),
#         'tomorrow': str(date.today() + datetime.timedelta(days=1)),
#         'day_after_tomorrow': str(date.today() + datetime.timedelta(days=2)),
#     }
#
#     if request.GET == {} or request.method == 'POST':
#         diet_form = DietChoiceForm({'type_of_diet': 'ovd'})
#         diet = 'ovd'
#         date_get = str(date.today())
#
#         meal = 'breakfast'
#
#     else:
#         diet = request.GET['input_type_of_diet']
#         date_get = request.GET['date']
#
#         diet_form = DietChoiceForm(request.GET)
#         meal = request.GET['meal']
#     day_of_the_week = get_day_of_the_week(date_get)
#     translated_diet = translate_diet(diet)
#
#     products_lp: tuple = creating_meal_menu_lp(day_of_the_week, translated_diet, meal)
#
#     products_main, products_garnish, products_salad, \
#     products_soup, products_porridge, products_dessert, \
#     products_fruit, products_drink = products_lp
#
#     products_cafe: tuple = creating_meal_menu_cafe(date_get, diet, meal)
#
#     queryset_main_dishes, queryset_garnish, queryset_salad, \
#     queryset_soup = products_cafe
#
#     formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')
#
#     if request.method == 'POST' and 'change-email' in request.POST:
#         # сhange_password(request.POST['changed-email'], request)
#
#         user = CustomUser.objects.get(id=request.user.id)
#         user.email = request.POST['changed-email']
#         user.username = request.POST['changed-email']
#         user.save()
#         request.user.email = request.POST['changed-email']
#         data = {
#             'diet_form': diet_form,
#             'date_menu': date_menu,
#             'products_main': products_main + queryset_main_dishes,
#             'products_porridge': products_porridge,
#             'products_dessert': products_dessert,
#             'products_fruit': products_fruit,
#             'products_garnish': products_garnish + queryset_garnish,
#             'products_salad': products_salad + queryset_salad,
#             'products_soup': products_soup + queryset_soup,
#             'products_drink': products_drink,
#             'page': page,
#             'date_get': date_get,
#             'formatted_date': formatted_date,
#             'meal': meal,
#             'modal': 'profile-edited',
#             'type': type
#         }
#         return render(request, 'menu.html', context=data)
#
#     if request.method == 'POST' and 'changed-password' in request.POST:
#         user = CustomUser.objects.get(id=request.user.id)
#         user.set_password(request.POST['changed-password'])
#         user.save()
#         data = {
#             'diet_form': diet_form,
#             'date_menu': date_menu,
#             'products_main': products_main + queryset_main_dishes,
#             'products_porridge': products_porridge,
#             'products_dessert': products_dessert,
#             'products_fruit': products_fruit,
#             'products_garnish': products_garnish + queryset_garnish,
#             'products_salad': products_salad + queryset_salad,
#             'products_soup': products_soup + queryset_soup,
#             'products_drink': products_drink,
#             'page': page,
#             'date_get': date_get,
#             'formatted_date': formatted_date,
#             'meal': meal,
#             'modal': 'password-edited',
#             'type': type
#         }
#         return render(request, 'menu.html', context=data)
#
#     data = {'diet_form': diet_form,
#             'date_menu': date_menu,
#             'products_main': products_main + queryset_main_dishes,
#             'products_porridge': products_porridge,
#             'products_dessert': products_dessert,
#             'products_fruit': products_fruit,
#             'products_garnish': products_garnish + queryset_garnish,
#             'products_salad': products_salad + queryset_salad,
#             'products_soup': products_soup + queryset_soup,
#             'products_drink': products_drink,
#             'page': page,
#             'date_get': date_get,
#             'formatted_date': formatted_date,
#             'meal': meal,
#             'diet': diet,
#             'type': type
#             }
#     return render(request, 'menu.html', context=data)