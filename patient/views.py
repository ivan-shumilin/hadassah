from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from doctor.forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp
from nutritionist.forms import TimetableForm
import random, calendar, datetime
from datetime import datetime, date, timedelta
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat
from dateutil.parser import parse
from django.db.models.functions import Lower
from doctor.functions import sorting_dishes, parsing, get_day_of_the_week, translate_diet
from patient.functions import formation_menu
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response


def group_patient_check(user):
    return user.groups.filter(name='patients').exists()


@login_required
@user_passes_test(group_patient_check, login_url='login')
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
    if request.GET == {} or request.method == 'POST':
        date_get = str(date.today())
        meal = 'breakfast'
    else:
        date_get = request.GET['date']
        meal = request.GET['meal']
    day_of_the_week = get_day_of_the_week(date_get)

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



    formatted_date = dateformat.format(date.fromisoformat(date_get), 'd E, l')
    data = {'user': user,
            'breakfast': breakfast,
            'afternoon': afternoon,
            'lunch': lunch,
            'dinner': dinner,
            'date_menu': date_menu,
            'page': page,
            'date_get': date_get,
            'formatted_date': formatted_date,
            }

    return render(request, 'patient_.html', context=data)

def test(request):
    return render(request, 'test.html', {})
