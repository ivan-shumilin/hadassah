from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *

class TimetableForm(ModelForm):
    class Meta:
        model = Timetable
        fields = ['datetime']

        widgets = {
            "datetime": DateInput(attrs={
                'type': 'date',
                'class': 'form-conrol',
            })
        }


class UserPasswordResetForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Виктор'}))
    lastname = forms.CharField(label='Фамилия', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'mail@example.com'}))
    # password = forms.CharField(label='Password',
    #                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    # password_repeat = forms.CharField(label='Repeat password',
    #                             widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль еще раз'}))

    class Meta:
        model = CustomUser
        fields = ('lastname', 'name', 'email',)

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password_repeat']

    def clean_name(self):
        valid_symbols = set("qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю() -,\'")
        cd = self.cleaned_data
        name = set(cd['name'].lower())
        if (name - valid_symbols) != set():
            raise forms.ValidationError(f'Недопустимые значения: {", ".join(name - valid_symbols)}.')
        return cd['name']


class UserloginForm(forms.ModelForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'mail@example.com'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль', 'style': 'margin-top: 10px;'}))

    # attrs = {'class': 'form-control'}
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'comment')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'comment')


class PatientRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО пациента', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Иванов Виктор Иванович'}))
    comment = forms.CharField(label='Комментарий', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Комментарий'}))
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