from collections import OrderedDict

from PIL import Image
from django.db import transaction, models
from django.db.models import Value
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput, CheckboxInput
from drf_spectacular.utils import extend_schema_view, extend_schema

from nutritionist.functions.get_ingredients import get_semifinished, get_semifinished_level_1, get_ingredients_for_ttk, \
    caching_ingredients
from nutritionist.serializers import GetIngredientsSerializer
from .forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, BotChatId, СhangesUsersToday, \
    UsersToday, TimetableLp, Ingredient, MenuByDayReadyOrder, UsersReadyOrder, ModifiedDish, Report, IngredientСache
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
    get_occupied_rooms, creates_dict_with_menu_patients_on_day_test, what_type_order, get_order_status, get_user_name, \
    translate_first_meal, add_features, next_meal
from doctor.functions.bot import check_change, do_messang_send, formatting_full_name
from doctor.functions.for_print_forms import create_user_today, check_time, update_UsersToday, update_СhangesUsersToday, \
    applies_changes, create_user_tomorrow, create_ready_order, create_report, create_products_lp, add_products_lp, \
    add_products_lp, create_product_storage
from doctor.functions.diet_formation import add_menu_three_days_ahead, update_diet_bd, \
    add_the_patient_emergency_food_to_the_database, get_meal_emergency_food
from doctor.functions.translator import get_day_of_the_week, translate_diet
from django.db.models import Q, F, Case, When, Value
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import management
import telepot
from doctor.tasks import send_messang, my_job_create_ready_order_dinner, my_job_send_messang_changes, \
    send_messang_changes
from .functions.download import get_token, download, get_ingredients
from .functions.helpers import formatting_full_name_mode_full
from .logic.create_ingredient import create_ingredients

from django.shortcuts import render
from django.views.generic import TemplateView

from .serializer import DishesSerializer, PatientsSerializer, InfoPatientSerializer, InputDataSerializer, \
    AddDishSerializer, ChangeDishSerializer, CroppImageSerializer, SendPatientProductsAPIViewSerializer, \
    UpdateSearchAPIViewSerializer, ProductsSerializer, CheckIsHavePatientSerializer


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
            imageLinks=product["imageLinks"],
            code=product["code"],
            description=product["description"],
            fatAmount=product["fatAmount"],
            proteinsAmount=product["proteinsAmount"],
            carbohydratesAmount=product["carbohydratesAmount"],
            energyAmount=product["energyAmount"],
            fatFullAmount=product["fatFullAmount"],
            proteinsFullAmount=product["proteinsFullAmount"],
            carbohydratesFullAmount=product["carbohydratesFullAmount"],
            energyFullAmount=product["energyFullAmount"],
            weight=product["weight"],
            groupId=product["groupId"],
            productCategoryId=product["productCategoryId"],
            type=product["type"],
            orderItemType=product["orderItemType"],
            measureUnit=product["measureUnit"],
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
                                                 'is_pureed_nutrition', 'is_without_lactose', 'type_pay',
                                                 'extra_bouillon'),
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
                                             extra=0, )

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
    # 11
    if request.method == 'POST' and 'add_patient' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        first_meal_user, data, patient_receipt_date, patient_receipt_time, meal_order = create_user(user_form, request)
        # нерабочие часы
        time = datetime.today().time()
        # если нужно экстренное питание добавим в эту переменную
        need_emergency_food = False
        # если время госпитализации пациента попадает на нерабочее время
        if patient_receipt_time.hour >= 18 or patient_receipt_time.hour <= 8 and meal_order == 'завтра':
            need_emergency_food = '&no_working_hours'
        if patient_receipt_time.hour >= 18 or patient_receipt_time.hour <= 7 and meal_order == 'завтрака':
            need_emergency_food = '&no_working_hours'
        # если рабочее время кухни
        if time.hour <= 17 or time.hour >= 9 and need_emergency_food != '&no_working_hours':
            meal_emergency_food = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
            if meal_emergency_food:
                need_emergency_food = f'&{meal_emergency_food}'
        if need_emergency_food:
            messages.add_message(request, messages.INFO, first_meal_user)
            messages.add_message(request, messages.INFO, 'patient-added')
            messages.add_message(request, messages.INFO, data + need_emergency_food)
        else:
            messages.add_message(request, messages.INFO, 'first')
            messages.add_message(request, messages.INFO, 'patient-added-2')
            messages.add_message(request, messages.INFO, 'last')
        return HttpResponseRedirect(reverse('doctor'))

    if request.method == 'POST' and 'edit_patient_flag' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        first_meal_user, data, patient_receipt_date, patient_receipt_time, is_edited, emergency_food = edit_user(
            user_form, 'edit', request)
        # если нужно экстренное питание добавим в эту переменную
        need_emergency_food = ""
        if is_edited:
            type_pop_up = 'patient-edited-2'
            # если меняем с нулевой диеты
            if emergency_food:
                # нерабочие часы
                time = datetime.today().time()

                if time.hour >= 18 or time.hour <= 8:
                    need_emergency_food = '&no_working_hours'
                else:
                    # если рабочие часы
                    meal_emergency_food = get_meal_emergency_food()
                    if meal_emergency_food:
                        need_emergency_food = f'&{meal_emergency_food}'
                if need_emergency_food:
                    type_pop_up = 'patient-edited'

            messages.add_message(request, messages.INFO, first_meal_user)
            messages.add_message(request, messages.INFO, type_pop_up)
            messages.add_message(request, messages.INFO, data + need_emergency_food)
        return HttpResponseRedirect(reverse('doctor'))

    if request.method == 'POST' and 'archive' in request.POST:
        id_user = request.POST.getlist('id_edit_user')[0]
        user = CustomUser.objects.get(id=id_user)
        modal = archiving_user(user, request)
        messages.add_message(request, messages.INFO, 'first')
        messages.add_message(request, messages.INFO, modal)
        messages.add_message(request, messages.INFO, 'last')
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
                                                 'full_name', 'birthdate', 'receipt_date', 'receipt_time', 'department',
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
    queryset = CustomUser.objects.filter(status='patient_archive').distinct('full_name').order_by(filter_by)
    # если есть поисковый запрос, то фильтруем по нему
    count: int = 80
    search_query_filter: Q = Q()
    search_query: str = ''
    try:
        search_query = request.POST.getlist('search')[0]
        search_query_filter = Q(full_name__icontains=search_query)
        count: int = 120
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
        first_meal_user, data, patient_receipt_date, patient_receipt_time, is_archive, emergency_food = edit_user(
            user_form, 'restore', request)
        if is_archive:
            # нерабочие часы
            time = datetime.today().time()
            # если нужно экстренное питание добавим в эту переменную
            need_emergency_food = False
            if time.hour >= 18 or time.hour <= 8:
                need_emergency_food = '&no_working_hours'
            else:
                meal_emergency_food = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
                if meal_emergency_food:
                    need_emergency_food = f'&{meal_emergency_food}'
            if need_emergency_food:
                messages.add_message(request, messages.INFO, first_meal_user)
                messages.add_message(request, messages.INFO, 'patient-restored')
                messages.add_message(request, messages.INFO, data + need_emergency_food)
            else:
                messages.add_message(request, messages.INFO, 'first')
                messages.add_message(request, messages.INFO, 'patient-restored-2')
                messages.add_message(request, messages.INFO, 'last')
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
        'search_query': search_query,
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
    diet_form: None = None
    date_menu = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + datetime.timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + datetime.timedelta(days=2)),
    }

    if request.GET == {} or request.method == 'POST':
        # diet_form = DietChoiceForm({'type_of_diet': 'ОВД'})
        diet = 'ОВД'
        date_get = str(date.today())
        meal = 'breakfast'
        sing = 'none'  # признак
    else:
        diet = request.GET['input_type_of_diet']
        date_get = request.GET['date']
        # diet_form = DietChoiceForm(request.GET)
        meal = request.GET['meal']
        sing = request.GET.get('sing', 'none')

    diet = diet.replace(" (Э)", "").replace(" (П)", "")

    if diet == 'БД':
        if date_get == date_menu['today']:
            day_of_the_week = 'понедельник'
        else:
            day_of_the_week = 'вторник'
            date_get = date_menu['tomorrow']
    else:
        day_of_the_week = get_day_of_the_week(date_get)

    if sing == 'is_probe':
        diet += " (Э)"

    if sing == 'is_pureed_nutrition':
        diet += " (П)"

    products_lp: tuple = creating_meal_menu_lp(day_of_the_week, diet, meal)

    products_main, products_garnish, products_salad, \
        products_soup, products_porridge, products_dessert, \
        products_fruit, products_drink = products_lp

    if diet not in ['ОВД веган (пост) без глютена', 'Нулевая диета', 'БД', 'Безйодовая', 'ПЭТ/КТ'] \
            and diet == diet.replace(" (Э)", "").replace(" (П)", ""):
        # для поиска блюд раздачи нужна диета на лат-ом ("ovd", ..)
        translated_diet = translate_diet(diet)
        products_cafe: tuple = creating_meal_menu_cafe(date_get, translated_diet, meal)
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
            'sing': sing,
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
            'sing': sing,

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
            'sing': sing,
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


# 333
class SendPatientProductsAPIView(APIView):
    def post(self, request):
        serializer = SendPatientProductsAPIViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data['id_user']
        date_show = serializer.validated_data['date_show']
        products = serializer.validated_data['products']
        meal = serializer.validated_data['meal']
        user_name = serializer.validated_data['user_name']
        comment = serializer.validated_data['comment']

        meal = translate_meal(meal).lower()
        patient = CustomUser.objects.get(id=patient_id)
        full_name = formatting_full_name(patient.full_name)
        user_name = formatting_full_name(user_name)

        room_number = ', ' + patient.room_number if patient.room_number != 'Не выбрано' else ''

        messang = f'<b>Корректировка для экстренной госпитализации:</b>\n'
        messang += f'   \n'
        messang += f'{full_name}{room_number}\n'
        messang += f'{patient.type_of_diet}, {meal}\n'
        messang += f'Комментарий: {comment}\n' if comment != '' else ''
        messang += f'   \n'
        for product_name in products.strip('&?&').split('&?&'):
            messang += f'– {product_name}\n'

        messang += f'({user_name})'
        # send_messang_changes(messang, settings.BOT_ID_EMERGEBCY_FOOD)
        my_job_send_messang_changes.delay(messang, settings.BOT_ID_EMERGEBCY_FOOD)

        return Response('ok')


class UpdateSearchAPIView(APIView):
    def post(self, request):
        serializer = UpdateSearchAPIViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_menu = serializer.validated_data['type']
        category = serializer.validated_data['cat']

        product_lp: list = []
        product_cafe: list = []

        if type_menu in ['lp', 'all']:
            filter: Q = Q(category__in=get_category(category)) if category != 'all' else Q()

            product_lp = list(ProductLp.objects.filter(
                filter
            ).annotate(
                cooking_method_annotation=Value("Отсутствует", output_field=models.CharField()),
                description_annotation=Case(
                    When(description__isnull=True, then=Value("Отсутствует")),
                    default=F('description'),
                    output_field=models.CharField()
                ),
                id_annotetion=F('id'),
            ).values(
                'name',
                'id',
                'number_tk',
                'description_annotation',
                'carbohydrate',
                'fat',
                'fiber',
                'energy',
                'cooking_method_annotation',
                'id_annotetion',
            ))

        if type_menu in ['cafe', 'all']:
            filter: Q = Q(category__in=get_category_cafe_2(category)) if category != 'all' else Q()

            product_cafe = list(Product.objects.filter(
                filter
            ).annotate(
                number_tk=F('iditem'),
                cooking_method_annotation=Case(
                    When(cooking_method__isnull=True, then=Value("Отсутствует")),
                    default=F('cooking_method'),
                    output_field=models.CharField()
                ),
                description_annotation=Case(
                    When(description__isnull=True, then=Value("Отсутствует")),
                    default=F('description'),
                    output_field=models.CharField()
                ),
                id_annotetion=F('id'),
            ).values(
                'name',
                'id',
                'number_tk',
                'description_annotation',
                'carbohydrate',
                'fat',
                'fiber',
                'energy',
                'cooking_method_annotation',
                'id_annotetion'
            ))

            # добавляем префикс к id для категории "Кафе"
            for p in list(product_cafe):
                p['id'] = f'cafe-cat-{p["id"]}'

        products = product_lp + product_cafe

        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)


class SendEmergencyFoodAPIView(APIView):
    MENU = {
        'without_sugar': 569,
        'standard': 568,
        'snack': 570,
    }

    def post(self, request):
        # получаем id пациента и первый прием пищи
        data = request.data['data']
        data = data.split('&')
        patient_id = data[0]
        first_meal = translate_first_meal(data[1])
        # если нерабочие часы no_working_hours, если рабочии приходит прием пищи, который нужно добавить
        data_no_name = data[2]
        user_name = request.data['user_name']
        user_name = formatting_full_name(user_name)

        patient = CustomUser.objects.get(id=patient_id)
        full_name = formatting_full_name(patient.full_name)
        comment = add_features(patient.comment,
                               patient.is_probe,
                               patient.is_without_salt,
                               patient.is_without_lactose,
                               patient.is_pureed_nutrition)

        room_number = ', ' + patient.room_number if patient.room_number != 'Не выбрано' else ''
        diet_without_sugar = [
            'ШД без сахара',
            'ОВД без сахара',
            'ШД без сахара (П)',
            'ОВД без сахара (Э)',
            'ШД без сахара (П)',
            'ОВД без сахара (Э)',
        ]
        # если нерабочие часы
        if data_no_name == 'no_working_hours':
            type_diet = 'without_sugar' if patient.type_of_diet in diet_without_sugar else 'without_sugar'
            # получаем рацион для пациента
            product_add: list = []
            if type_diet == 'without_sugar':
                product_add.append(self.MENU['without_sugar'])
            else:
                product_add.append(self.MENU['standard'])

            if not patient.is_probe and not patient.is_pureed_nutrition:
                product_add.append(self.MENU['snack'])

            # записываем отчет на завтра
            time = datetime.today().time()
            if time.hour >= 18 or time.hour == 0:
                date_create = date.today() + timedelta(days=1)
            else:
                date_create = date.today()

        # если рабочие часы
        else:
            meal = data_no_name
            # добавить прием пищи в MenuByDayReadyOrder и в MenuByDay
            date_today = str(date.today())
            product_add: list = add_the_patient_emergency_food_to_the_database(patient, date_today, meal,
                                                                               extra_bouillon=False)
            date_create = patient.receipt_date

        # добавить в отчеты и отправить сообщение
        meal_mod = ', ' + translate_meal(meal).lower() if data_no_name != 'no_working_hours' else ''
        messang = f'<b>Доп. питание для экстренной госпитализации:</b>\n'
        messang += f'    \n'
        messang += f'{full_name}{room_number}\n'
        messang += f'{patient.type_of_diet}{meal_mod}\n'
        messang += f'Комментарий: {comment}\n' if comment != '' else ''
        messang += f'    \n'
        type_report = 'emergency-night' if data_no_name == 'no_working_hours' else 'emergency-day'
        first_meal = next_meal(first_meal) if type_report == 'emergency-day' else first_meal

        for product_id in product_add:
            messang += f'– {ProductLp.objects.get(id=product_id).name}\n'
            Report(user_id=patient,
                   date_create=date_create,
                   meal=first_meal,
                   product_id=product_id,
                   type_of_diet=patient.type_of_diet,
                   type=type_report).save()

        messang += f'({user_name})'
        # send_messang_changes(messang, settings.BOT_ID_EMERGEBCY_FOOD)
        my_job_send_messang_changes.delay(messang, settings.BOT_ID_EMERGEBCY_FOOD)
        check_mark = '&#8505;'
        messang = f'{check_mark} <b>Изменение с {translate_meal(meal).lower() + "а"}</b>\n'
        messang += f'Экстренное питание для {full_name} {patient.type_of_diet}\n'
        messang += f'({user_name})'
        # send_messang_changes(messang, settings.BOT_ID_EMERGEBCY_FOOD)
        my_job_send_messang_changes.delay(messang)

        return Response('ok')


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


def get_category_cafe_2(category):
    categorys = {
        "salad": ["Салаты"],
        "soup": ["Первые блюда"],
        "porridge": ["Каши"],
        "main": ["Завтраки", "Вторые блюда", "Блюда от шефа"],
        "garnish": ["Гарниры"],
        "dessert": ["Десерты"],
    }
    return categorys.get(category, [])


def get_category_by_id(id_product):
    if 'cafe' in id_product:
        category_name = Product.objects.get(id=id_product.split('-')[2]).category
    else:
        category_name = ProductLp.objects.get(id=id_product).category
    return get_category_product(category_name)


def get_category_product(category_name):
    category_mapping = {
        'salad': ["салат", "Салаты"],
        'soup': ["суп", "Первые блюда"],
        'porridge': ["каша", "Каши"],
        'main': ["основной", "Завтраки", "Вторые блюда", "Блюда от шефа"],
        'garnish': ["гарнир", "Гарниры"],
        'dessert': ["десерт"],
        'fruit': ["фрукты"],
        'drink': ["напиток"],
        'products': ["товар", "hidden"],
        'hidden': ["hidden"],
        'bouillon': ["бульон"],
    }

    for category, values in category_mapping.items():
        if category_name in values:
            return category

    return None


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
            'Безйодовая',
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
            ]),
            OrderedDict([
                ('name', 'Салат из огурцов и помидоров 150 гр'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 551),
                ('description', '')
            ]),
            OrderedDict([
                ('name', 'Рис "Басмати" 150 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 565),
                ('description', 'Рис "Басмати" 150 гр')
            ]),
            OrderedDict([
                ('name', 'Филе лосося на пару 90 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 564),
                ('description', 'Семга филе, соль, перец черный молотый, сок лимона, зелень.')
            ]),
            OrderedDict([
                ('name', 'Митбол с кабачком 100 гр'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 563),
                ('description',
                 'Кабачки/цукини, масло  подсолнечное, фарш курица/говядина( говядина, курица, молоко3,2 % , хлеб, чеснок, соль)')
            ]),
            OrderedDict([
                ('name', 'Куриная грудка 200 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 575),
                ('description', '')
            ]),
            OrderedDict([
                ('name', 'Котлета из трески 100 гр'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 566),
                ('description',
                 'Фарш рыбный ( филе трески , филе минтая, соль, перец, хлеб, яйцо куриное, зелень), мука пшеничная, масло подсолнечное.')
            ]),
            OrderedDict([
                ('name', 'Кабачки запеченные 150 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 574),
                ('description', ' ')
            ]),
            OrderedDict([
                ('name', 'Суфле из отварной говядины (ЩД) 115 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 348),
                ('description', ' ')
            ]),
            OrderedDict([
                ('name', 'Гречка отварная 150 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 463),
                ('description', 'Масло подсолнечное, соль, вода для производства, гречка')
            ]),
            OrderedDict([
                ('name', 'Яйцо куриное отварное 1 шт.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 577),
                ('description', 'Яйцо куриное')
            ]),
            OrderedDict([
                ('name', 'Тофники  120 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 521),
                ('description', 'Тофники замороженные')
            ]),
            OrderedDict([
                ('name', 'Сметана 15% 40 гр.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 474),
                ('description', 'Сметана 15%')
            ]),
            OrderedDict([
                ('name', 'Блин 2 шт.'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 579),
                ('description',
                 'Масло подсолнечное, тесто для блинов (молоко 3,2%, яйцо куриное, масло подсолнечное, сахар песок, соль, мука пшеничная)')
            ]),
            OrderedDict([
                ('name', 'Кефир 200 мл'),
                ('type_of_diet', 'Безйодовая'),
                ('id', 580),
                ('description', 'Кефир')
            ]),

        ]
        data = {
            "dishes_all": dishes_all,
            "dishes_meal": dishes_meal,
            "dishes_cafe": dishes_cafe,
            "dishes_no_active_diet": dishes_no_active_diet,
            "other": other
        }
        return Response(data)


class DeleteDishAPIView(APIView):
    logger = logging.getLogger('main_logger')

    def delete(self, request):
        serializer = AddDishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_user: str = serializer.validated_data['id_user']
        date = serializer.validated_data['date']
        product_id: str = serializer.validated_data['product_id']
        category: str = serializer.validated_data['category']
        meal: str = serializer.validated_data['meal']
        doctor: str = serializer.validated_data['doctor']

        changes: list = []  # список с меню в который надо внести изменения
        product_name = get_product_by_id(product_id)

        # Проверка времани, если заказ уже сформирован (менее 2х часов до приема пищи)
        # вносить изменения в MenuByDayReadyOrder
        order_status: str = get_order_status(meal, date)
        menu = MenuByDay.objects.all()
        changes.append((menu, id_user))

        table = "MenuByDay"
        patient = CustomUser.objects.get(id=id_user)

        if order_status == 'fix-order':
            menu = MenuByDayReadyOrder.objects.all()
            patient = UsersReadyOrder.objects.filter(user_id=id_user).first()
            changes.append((menu, patient))
            table = "MenuByDayReadyOrder"
        with transaction.atomic():
            for menu, id in changes:
                try:
                    item_menu = menu.get(user_id=id, date=date, meal=meal)
                except:
                    message = logging_delete_dish_api('Cant find menu',
                                                      table, order_status, product_name, product_id,
                                                      meal, patient, category, date, doctor
                                                      )
                    self.logger.error(message)
                    return Response({'status': 'Error'})

                products = getattr(item_menu, category)
                products = products.split(',')
                products.remove(product_id)
                products = ','.join(products)
                setattr(item_menu, category, products)
                item_menu.save()
                message = logging_delete_dish_api('Save',
                                                  table, order_status, product_name, product_id,
                                                  meal, patient, category, date, doctor
                                                  )
                self.logger.info(message)
            # удалить из ModifiedDish если есть
            patient = CustomUser.objects.filter(id=id_user).first()
            try:
                ModifiedDish.objects \
                    .filter(product_id=product_id, date=date, meal=meal, user_id=patient).first().delete()
            except:
                message = logging_delete_dish_api('Cant delete',
                                                  table, order_status, product_name, product_id,
                                                  meal, patient, category, date, doctor
                                                  )
                self.logger.error(message)
                pass

            message = logging_delete_dish_api('Delete ',
                                              table, order_status, product_name, product_id,
                                              meal, patient, category, date, doctor
                                              )
            self.logger.info(message)

            return Response({'status': 'OK'})


class CheckIsHavePatientAPIView(APIView):
    """
    Проверяет, есть ли пациент с указаными ФИО и датой рожения.
    Если есть, то в архиве или в активных пациентах.
    """

    def post(self, request):
        serializer = CheckIsHavePatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        full_name: str = serializer.validated_data['full_name']
        birthdate: datetime = serializer.validated_data['birthdate']

        full_name = formatting_full_name_mode_full(full_name)
        qs: Q = CustomUser.objects.filter(
            full_name=full_name,
            birthdate=birthdate,
        )

        if qs.filte(status='patient').exists():
            response = {'status': 'patient'}
        elif qs.filte(status='patient_archive').exists():
            response = {'status': 'patient_archive'}
        else:
            response = {'status': 'None'}
        return Response(response)


def get_product_by_id(string_id: [str, int]) -> str:
    """ Возвращает название продукта по его id """
    if 'cafe-cat' in string_id:
        id = string_id.split('-')[-1]
        return Product.objects.get(id=id).name
    return ProductLp.objects.get(id=string_id).name


class AddDishAPIView(APIView):
    logger = logging.getLogger('main_logger')

    def post(self, request):
        serializer = AddDishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_user: str = serializer.validated_data['id_user']
        date = serializer.validated_data['date']
        product_id: str = serializer.validated_data['product_id']
        category: str = serializer.validated_data['category']
        meal: str = serializer.validated_data['meal']
        doctor: str = serializer.validated_data['doctor']

        product_name = get_product_by_id(product_id)
        changes: list = []  # список с меню в который надо внести изменения

        # Проверка времани, если заказ уже сформирован (менее 2х часов до приема пищи)
        # вносить изменения в MenuByDayReadyOrder
        # type_order = what_type_order()
        order_status: str = get_order_status(meal, date)
        menu = MenuByDay.objects.all()
        table = "MenuByDay"
        changes.append((menu, id_user))
        patient = CustomUser.objects.get(id=id_user)

        if order_status == 'fix-order':
            menu = MenuByDayReadyOrder.objects.all()
            patient = UsersReadyOrder.objects.filter(user_id=id_user).first()
            changes.append((menu, patient))
            table = "MenuByDayReadyOrder"
        with transaction.atomic():
            for menu, id in changes:
                try:
                    item_menu = menu.get(user_id=id, date=date, meal=meal)
                except:
                    message = logging_add_dish_api('Cant find menu',
                                                   table, order_status, product_name,
                                                   product_id, meal, patient, category, date,
                                                   doctor)
                    self.logger.error(message)
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

                message = logging_add_dish_api('Save ',
                                               table, order_status, product_name,
                                               product_id, meal, patient, category, date,
                                               doctor)
                self.logger.info(message)
            # добавить изменения в ModifiedDish
            user = CustomUser.objects.get(id=id_user)
            ModifiedDish(product_id=product_id, date=date, meal=meal, user_id=user, status="add").save()
            table = "ModifiedDish"
            message = logging_add_dish_api('Save',
                                           table, order_status, product_name,
                                           product_id, meal, patient, category, date,
                                           doctor)
            self.logger.info(message)
        return Response({'status': 'OK'})


class ChangeDishAPIView(APIView):
    logger = logging.getLogger('main_logger')

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
        doctor: str = serializer.validated_data['doctor']

        message = ''

        # Проверка времани, если заказ уже сформирован (менее 2х часов до приема пищи)
        # вносить изменения в MenuByDayReadyOrder
        order_status: str = get_order_status(meal, date)
        menu = MenuByDay.objects.all()
        changes.append((menu, id_user))

        product_name_add = get_product_by_id(product_id_add)
        product_name_del = get_product_by_id(product_id_del)

        table = "MenuByDay"
        if order_status == 'fix-order':
            menu = MenuByDayReadyOrder.objects.all()
            patient = UsersReadyOrder.objects.filter(user_id=id_user).first()
            changes.append((menu, patient))
            table = "MenuByDayReadyOrder"
        with transaction.atomic():
            patient = CustomUser.objects.filter(id=id_user).first()
            for menu, id in changes:
                try:
                    with transaction.atomic():
                        item_menu = menu.select_for_update().get(user_id=id, date=date, meal=meal)
                        # удаление блюда
                        products = getattr(item_menu, category)
                        products = products.split(',')
                        products.remove(product_id_del)
                        products = ','.join(products)
                        setattr(item_menu, category, products)

                        # добавление блюда
                        # получение категории блюда
                        category_add = get_category_by_id(product_id_add)
                        products = getattr(item_menu, category_add)
                        if products == "":
                            products = product_id_add
                        else:
                            products = products.split(',')
                            products.append(product_id_add)
                            products = ','.join(products)
                        setattr(item_menu, category_add, products)
                        item_menu.save()

                except:
                    category_add = get_category_by_id(product_id_add)
                    message = logging_change_dish_api('Cant change dish', table, order_status,
                                                      product_name_add,
                                                      product_id_add, product_name_del, product_id_del, meal, patient,
                                                      category_add,
                                                      category, date, doctor)
                    self.logger.error(message)

                    return Response({'status': 'Error'})
            # удалить из ModifiedDish если есть
            patient = CustomUser.objects.filter(id=id_user).first()
            try:
                ModifiedDish.objects \
                    .filter(product_id=product_id_del, date=date, meal=meal, user_id=patient).first().delete()
            except:
                message = logging_change_dish_api('Cant delete', table, order_status, product_name_add,
                                                  product_id_add, product_name_del, product_id_del, meal, patient,
                                                  category_add,
                                                  category, date, doctor)
                self.logger.error(message)
                pass
            # добавить изменения в ModifiedDish
            user = CustomUser.objects.get(id=id_user)
            ModifiedDish(product_id=product_id_add, date=date, meal=meal, user_id=user, status="change").save()
            table = "ModifiedDish"

            message = logging_change_dish_api('Save', table, order_status, product_name_add,
                                              product_id_add, product_name_del, product_id_del, meal, patient,
                                              category_add,
                                              category, date, doctor)
            self.logger.info(message)

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

class GetIngredientsAPIView(APIView):
    def post(self, request):
        serializer = GetIngredientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        filter: dict = {}

        if data['filter'] == 'name':
            filter['filter_field'] = 'name'
        else:
            filter['filter_field'] = 'amount_out'
        filter['value'] = data['value']

        string = data['categories'].replace('&#x27;', '')
        lst = string[1:-1].split(', ')
        filter['categories'] = lst

        ingredients_all = IngredientСache.objects.filter(start=data['start'], end=data['end']).order_by(
            'create_at').last().ingredient
        ingredients: dict = {}
        is_reverse = False if filter['value'] == 'top' else True
        for key, value in ingredients_all.items():
            if value['category'] in filter['categories']:
                ingredients[key] = value

        ingredients = dict(sorted(
            ingredients.items(),
            key=lambda x: x[1][filter['filter_field']],
            reverse=is_reverse,
        ))

        categories = None
        response = json.dumps({'categories': categories, 'ingredients': ingredients})

        return Response(response)


class testAPIView(APIView):
    def get(self, request):
        caching_ingredients()
        return Response({'status': 'OK'})


def logging_add_dish_api(info, table, order_status, product_name, product_id,
                         meal, patient, category, date, author) -> str:
    """ Сообщение для логирования функции AddDishAPIView """

    message = (f'ADD DISH | {info} | '
               f'table: {table} | '
               f'status: {order_status} | '
               f'product: {product_name} (id: {product_id}) | '
               f'meal: {meal} | '
               f'patient: {patient.full_name} | '
               f'category: {category} | '
               f'date: {date} | '
               f'author: {author}')

    return message


def logging_change_dish_api(info, table, order_status, product_name_add, product_id_add,
                            product_name_del, product_id_del, meal, patient, category_add,
                            category, date, author) -> str:
    """ Сообщение для логирования ChangeDishAPIView """

    message = (f'CHANGE DISH | {info} | '
               f'table: {table} | '
               f'status: {order_status} | '
               f'product add: {product_name_add} (id: {product_id_add}) | '
               f'product delete: {product_name_del} (id: {product_id_del}) | '
               f'meal: {meal} | '
               f'patient: {patient.full_name} | '
               f'category add product: {category_add} | '
               f'category delete product: {category} | '
               f'date: {date} | '
               f'author: {author}')

    return message


def logging_delete_dish_api(info, table, order_status, product_name, product_id,
                            meal, patient, category, date, author) -> str:
    """ Сообщение для логирования DeleteDishAPIView """

    message = (f'DELETE DISH | {info} | '
               f'table: {table} | '
               f'status: {order_status} | '
               f'product: {product_name} (id: {product_id}) | '
               f'meal: {meal} | '
               f'patient: {patient.full_name} | '
               f'category: {category} | '
               f'date: {date} | '
               f'meal: {meal} | '
               f'author: {author}')

    return message
