from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from .forms import PatientRegistrationForm, DietChoiceForm
from nutritionist.models import CustomUser, Product, Timetable, ProductLp
from nutritionist.forms import TimetableForm
import random, calendar, datetime
import datetime
from datetime import datetime, date, timedelta
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat
from dateutil.parser import parse
from django.db.models.functions import Lower
from doctor.functions import sorting_dishes, parsing, get_day_of_the_week, translate_diet
from django.db.models import Q












def group_doctors_check(user):
    return user.groups.filter(name='doctors').exists()

filter_by = 'full_name' # дефолтная фильтрация
sorting = 'top'
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
    global filter_by
    global sorting
    page = 'menu-doctor'
    queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
    if request.method == 'POST' and 'filter_by_flag' in request.POST:

        if filter_by == request.POST.getlist('filter_by')[0]:
            if sorting == 'top':
                queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
                sorting = 'down'
            else:
                queryset = CustomUser.objects.filter(status='patient').order_by(f'-{filter_by}')
                sorting = 'top'

        else:
            filter_by = request.POST.getlist('filter_by')[0]
            queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
    if request.method == 'POST' and 'add_patient' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        formset = \
            CustomUserFormSet(request.POST, request.FILES, queryset=queryset)

        if user_form.is_valid():
            while True:
                login = ''.join([random.choice("123456789qwertyuiopasdfghjklzxcvbnm") for i in range(10)])
                try:
                    CustomUser.objects.get(id=login)
                    continue
                except Exception:
                    break
            user = CustomUser.objects.create_user(login)
            user.full_name = user_form.data['full_name']
            user.receipt_date = parse(user_form.data['receipt_date']).strftime('%Y-%m-%d')
            user.receipt_time = parse(user_form.data['receipt_time']).strftime('%h:%m')
            user.receipt_time = user_form.data['receipt_time']
            user.department = user_form.data['department']
            user.room_number = user_form.data['room_number']
            user.type_of_diet = user_form.data['type_of_diet']
            user.comment = user_form.data['comment']
            user.status = 'patient'
            user.save()
            queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
            formset = CustomUserFormSet(queryset=queryset)
            return render(request,
                           'doctor.html',
                          {'formset': formset,
                           'modal': 'patient-added',
                           'page': page,
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
    if request.method == 'POST' and 'edit_patient_flag' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        user = CustomUser.objects.get(id=user_form.data['id_edit_user'])
        user.full_name = user_form.data['full_name1']
        user.receipt_date = parse(user_form.data['receipt_date1']).strftime('%Y-%m-%d')
        user.receipt_time = user_form.data['receipt_time1']
        user.receipt_time = user_form.data['receipt_time1']
        user.department = user_form.data['department1']
        user.room_number = user_form.data['room_number1']
        user.type_of_diet = user_form.data['type_of_diet1']
        user.comment = user_form.data['comment1']
        user.save()
        formset = CustomUserFormSet(queryset=queryset)
        data = {
                'id_edited_user': user_form.data['id_edit_user'],
                'formset': formset,
                'page': page,
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
        user_form = PatientRegistrationForm(request.POST)
        formset = CustomUserFormSet(queryset=queryset)
        if not formset.is_valid():
            data = {
                'modal': 'archived',
                'formset': formset,
                'page': page,
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
                'formset': formset,
                'sorting': sorting,
                'user_form': user_form,
                'filter_by': filter_by
            }
        return render(request, 'doctor.html', context=data)
    user_form = PatientRegistrationForm()
    formset = CustomUserFormSet(queryset=queryset)
    data = {
            'formset': formset,
            'page': page,
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
                                              'receipt_date': DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
                                              'receipt_time': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
                                              'comment': TextInput(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),
                                              'id': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )


    page = 'menu-archive'
    global filter_by
    global sorting

    queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
    if request.method == 'POST' and 'filter_by_flag' in request.POST:

        if filter_by == request.POST.getlist('filter_by')[0]:
            if sorting == 'top':
                queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
                sorting = 'down'
            else:
                queryset = CustomUser.objects.filter(status='patient_archive').order_by(f'-{filter_by}')
                sorting = 'top'

        else:
            filter_by = request.POST.getlist('filter_by')[0]
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
        diet_form = DietChoiceForm({'type_of_diet': 'ОВД'})
        diet = 'ovd'
        date_get = str(date.today())
        meal = 'breakfast'

    else:
        diet = request.GET['type_of_diet']
        date_get = request.GET['date']
        diet_form = DietChoiceForm(request.GET)
        meal = request.GET['meal']
    day_of_the_week = get_day_of_the_week(date_get)
    translated_diet = translate_diet(diet)
    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))

    products_main = []
    products_porridge = []
    products_dessert = []
    products_fruit = []
    products_salad = []
    products_soup = []
    products_drink = []
    products_garnish = []

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

    if meal == 'breakfast':
        products_garnish = list(products.filter(category='гарнир'))
        products_main = list(products.filter(category='основной'))
        products_porridge = list(products.filter(category='каша'))

    if meal == 'afternoon':
        products_main = list(products.filter(category='основной'))
        products_dessert = list(products.filter(category='десерт'))
        products_fruit = list(products.filter(category='фрукты'))
        products_drink = list(products.filter(category='напиток'))

    if meal == 'lunch':
        products_main = list(products.filter(category='основной'))
        products_garnish = list(products.filter(category='гарнир'))
        products_salad = list(products.filter(category='салат'))
        products_soup = list(products.filter(category='суп'))
        products_drink = list(products.filter(category='напиток'))

    if meal == 'dinner':
        products_main = list(products.filter(category='основной'))
        products_garnish = list(products.filter(category='гарнир'))
        products_drink = list(products.filter(category='напиток'))


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
            }
    return render(request, 'menu.html', context=data)

def menu_test(request):
    return render(request, 'menu_test.html', {})