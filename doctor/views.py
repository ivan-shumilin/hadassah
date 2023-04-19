from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput, CheckboxInput
from .forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, BotChatId, СhangesUsersToday, \
    UsersToday, TimetableLp, Ingredient
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
    get_occupied_rooms
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

from .serializer import DishesSerializer


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

    if diet not in ['ОВД веган (пост) без глютена', 'Нулевая диета', 'БД', 'Безйодовая']:
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
        'salad': "салат",
        'soup': "суп",
        'porridge': "каша",
        'main': "основной",
        'garnish': "гарнир",
        'dessert': "десерт",
        'fruit': "фрукты",
        'drink': "напиток",
        'product': "товар"
    }
    return categorys[category]

@extend_schema_view(
    post=extend_schema(summary='Получение блюд из всех диет по категории на день ',
                       tags=['Меню: Все блюда по категрии']),
)
class GetAllDishesByCategoryAPIView(APIView):
    def get(self, request):
        category = request.GET['category']
        date = request.GET['date']
        day_of_the_week = get_day_of_the_week(date)
        category = get_category(category)
        dishes = TimetableLp.objects.filter(day_of_the_week=day_of_the_week,
                                            item__category=category
                                            ).distinct('item__name')
        serializer = DishesSerializer(dishes, many=True)
        return Response(serializer.data)



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