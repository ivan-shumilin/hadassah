from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.forms import Textarea, TextInput, Select, DateInput, TimeInput
from .forms import PatientRegistrationForm
from nutritionist.models import CustomUser, Product, Timetable
from nutritionist.forms import TimetableForm
import random, calendar, datetime
import datetime
from datetime import datetime, date, timedelta
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateformat


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

    filter_by = 'full_name' # дефолтная фильтрация
    if request.method == 'POST':
        filter_by = request.POST.getlist('filter_by')[0]

    queryset = CustomUser.objects.filter(status='patient').order_by(filter_by)
    if request.method == 'POST' and 'add_patient' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        formset = \
            CustomUserFormSet(request.POST, request.FILES, queryset=queryset)

        if user_form.is_valid():
            login = str(len(CustomUser.objects.all()) + 1)
            user = CustomUser.objects.create_user(login)
            user.full_name = user_form.data['full_name']
            user.receipt_date = user_form.data['receipt_date']
            user.receipt_time = user_form.data['receipt_time']
            user.department = user_form.data['department']
            user.room_number = user_form.data['room_number']
            user.type_of_diet = user_form.data['type_of_diet']
            user.comment = user_form.data['comment']
            user.status = 'patient'
            user.save()
            formset = CustomUserFormSet(queryset=queryset)
            return render(request,
                          'doctor.html',
                          {'formset': formset,
                           'user_form': user_form,
                           'filter_by': filter_by})

    if request.method == 'POST' and 'update' in request.POST:
        user_form = PatientRegistrationForm(request.POST)
        formset = \
            CustomUserFormSet(request.POST, request.FILES, queryset=queryset)
        if not formset.is_valid():
            data = {
                'formset': formset,
                'user_form': user_form,
                'filter_by': filter_by}
            return render(request, 'doctor.html', context=data)
        else:
            formset.save()
            data = {
                'formset': formset,
                'user_form': user_form,
                'filter_by': filter_by
            }
        return render(request, 'doctor.html', context=data)

    if request.method == 'POST' and 'archive' in request.POST:
        id_user = request.POST.getlist('archive')[0]
        user = CustomUser.objects.get(id=id_user)
        user.status = 'patient_archive'
        user.save()
        user_form = PatientRegistrationForm(request.POST)
        formset = \
            CustomUserFormSet(request.POST, request.FILES, queryset=queryset)
        if not formset.is_valid():
            data = {
                'formset': formset,
                'user_form': user_form,
                'filter_by': filter_by
            }
            return render(request, 'doctor.html', context=data)
        else:
            formset.save()
            queryset = CustomUser.objects.filter(status='patient')
            formset = CustomUserFormSet(queryset=queryset)
            data = {
                'formset': formset,
                'user_form': user_form,
                'filter_by': filter_by
            }
        return render(request, 'doctor.html', context=data)
    user_form = PatientRegistrationForm()
    formset = CustomUserFormSet(queryset=queryset)
    data = {
            'formset': formset,
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
    filter_by = 'full_name' # дефолтная фильтрация
    if request.method == 'POST':
        filter_by = request.POST.getlist('filter_by')[0]
    queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
    if request.method == 'POST' and 'archive' in request.POST:
        id_user = request.POST.getlist('archive')[0]
        user = CustomUser.objects.get(id=id_user)
        user.status = 'patient'
        user.save()
        user_form = PatientRegistrationForm(request.POST)
        formset = \
            CustomUserFormSet(request.POST, request.FILES, queryset=queryset)
        if not formset.is_valid():
            data = {
                'formset': formset,
                'user_form': user_form,
                'filter_by': filter_by,
            }
            return render(request, 'doctor.html', context=data)
        else:
            formset.save()
            queryset = CustomUser.objects.filter(status='patient_archive').order_by(filter_by)
            formset = CustomUserFormSet(queryset=queryset)
            data = {
                'formset': formset,
                'user_form': user_form,
                'filter_by': filter_by,
            }
        return render(request, 'archive.html', context=data)

    user_form = PatientRegistrationForm()
    formset = CustomUserFormSet(queryset=queryset)
    data = {
            'formset': formset,
            'user_form': user_form,
            'filter_by': filter_by,
    }
    return render(request, 'archive.html', context=data)


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def menu(request):
    import datetime
    if request.GET == {}:
        diet = 'ovd'
        date_menu = str(date.today() - datetime.timedelta(days=16))
    else:
        diet = request.GET['diet']
        date_menu = request.GET['date']
    today = str(date.today() - datetime.timedelta(days=16))
    tomorrow = str(date.today() - datetime.timedelta(days=15))
    day_after_tomorrow = str(date.today() - datetime.timedelta(days=14))
    queryset = Product.objects.filter(timetable__datetime=date_menu).filter(**{diet: 'True'})
    formatted_date = dateformat.format(date.fromisoformat(date_menu), settings.DATE_FORMAT)
    data = {'diet': diet,
            'products': queryset,
            'today': today,
            'tomorrow': tomorrow,
            'day_after_tomorrow': day_after_tomorrow,
            'date_menu': date_menu,
            'formatted_date': formatted_date
            }
    return render(request, 'menu.html', context=data)



