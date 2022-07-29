from django import forms
from nutritionist.models import CustomUser
from django.forms import ModelForm, DateInput
from doctor.choices import *


class PatientRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО пациента', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Иванов Виктор Иванович'}))
    receipt_date = forms.DateField(label='Дата госпитализации', widget=forms.DateInput(format='%Y-%m-%d',
        attrs={'class': 'form-control', 'type': 'date'}))
    receipt_time = forms.TimeField(label='Время госпитализации', widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))
    comment = forms.CharField(label='Комментарий', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Комментарий'}))
    department = forms.ChoiceField(label='Отделение', choices=TYPE_DEPARTMENT,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Не выбрано'})
                                   )
    room_number = forms.ChoiceField(label='Номер палаты', choices=ROOM_NUMBERS,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Не выбрано'})
                                   )
    type_of_diet = forms.ChoiceField(label='Диета', choices=TYPE_DIET,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Не выбрано'})
                                   )
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(
    #     attrs={'class': 'form-control', 'placeholder': 'mail@example.com'}))
    # password = forms.CharField(label='Password',
    #                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    # password_repeat = forms.CharField(label='Repeat password',
    #                             widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль еще раз'}))

    class Meta:
        model = CustomUser
        fields = ('full_name', 'comment',)

    def clean_full_name(self):
        valid_symbols = set("qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю() -,\'")
        cd = self.cleaned_data
        full_name = set(cd['full_name'].lower())
        if (full_name - valid_symbols) != set():
            raise forms.ValidationError(f'Недопустимые значения: {", ".join(full_name - valid_symbols)}.')
        return cd['full_name']