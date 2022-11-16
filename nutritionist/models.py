from django.db import models
from datetime import date
from datetime import datetime
import uuid
from django.contrib.auth.models import AbstractUser
from doctor.choices import *
from patient.choices import *


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200, null=True)
    birthdate = models.DateField(null=True)
    receipt_date = models.DateField(null=True)
    receipt_time = models.TimeField(null=True)
    floor = models.CharField(max_length=200, null=True)

    department = models.CharField(
        max_length=100,
        choices=TYPE_DEPARTMENT,
        blank=True,
        default='Не выбрано',
        help_text='Выбор отделения')

    room_number = models.CharField(
        max_length=100,
        choices=ROOM_NUMBERS,
        blank=True,
        default='200',
        help_text='Выбор номера палаты')


    bed = models.CharField(
        max_length=100,
        choices=BED,
        blank=True,
        default='200',
        help_text='Выбор койко-места')

    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')

    comment = models.CharField(
        max_length=1000,
        null=True,
        blank=True)

    status = models.CharField(
        max_length=100,
        choices=STATUS_PATIENT,
        blank=True,
        default='',
        help_text='Выбор диеты')


    def __str__(self):
        return f'{self.full_name}'

class UsersToday(models.Model):
    # таблица создаёться 1 раз в сутки, в 00:00.
    # все записи предыдущего для удаляються
    user_id = models.CharField(max_length=200, null=True)
    date_create = models.DateField(default=date.today)
    full_name = models.CharField(max_length=200, null=True)
    receipt_date = models.DateField(null=True)
    receipt_time = models.TimeField(null=True)

    department = models.CharField(
        max_length=100,
        choices=TYPE_DEPARTMENT,
        blank=True,
        default='Не выбрано',
        help_text='Выбор отделения')

    room_number = models.CharField(
        max_length=100,
        choices=ROOM_NUMBERS,
        blank=True,
        default='200',
        help_text='Выбор номера палаты')

    bed = models.CharField(
        max_length=100,
        choices=BED,
        blank=True,
        default='200',
        help_text='Выбор койко-места')

    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')

    comment = models.CharField(
        max_length=1000,
        null=True,
        blank=True)

    status = models.CharField(
        max_length=100,
        choices=STATUS_PATIENT,
        blank=True,
        default='',
        help_text='Выбор диеты')


    def __str__(self):
        return f'{self.full_name}'


class СhangesUsersToday(models.Model):
    # в таблицу записываеться изменения и время вступления изменений в силу
    user_id = models.CharField(max_length=200, null=True)
    date_create = models.DateField(default=date.today)
    time_change = models.CharField(
            max_length=100,
            choices=MEALS,
            blank=True,
            default='',
        )
    full_name = models.CharField(max_length=200, null=True)
    receipt_date = models.DateField(null=True)
    receipt_time = models.TimeField(null=True)

    department = models.CharField(
        max_length=100,
        choices=TYPE_DEPARTMENT,
        blank=True,
        default='Не выбрано',
        help_text='Выбор отделения')

    room_number = models.CharField(
        max_length=100,
        choices=ROOM_NUMBERS,
        blank=True,
        default='200',
        help_text='Выбор номера палаты')

    bed = models.CharField(
        max_length=100,
        choices=BED,
        blank=True,
        default='200',
        help_text='Выбор койко-места')

    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')

    comment = models.CharField(
        max_length=1000,
        null=True,
        blank=True)

    status = models.CharField(
        max_length=100,
        choices=STATUS_PATIENT,
        blank=True,
        default='',
        help_text='Выбор диеты')


    def __str__(self):
        return f'{self.full_name}'


class Base(models.Model):
    date_create = models.DateField(default=date.today)
    base = models.CharField(max_length=5000000, null=True)

    def __str__(self):
        return f'{self.base}'


class Product(models.Model):
    iditem = models.IntegerField(null=True)
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    carbohydrate = models.CharField(max_length=200, null=True)
    fat = models.CharField(max_length=200, null=True)
    fiber = models.CharField(max_length=200, null=True)
    energy = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=2000, null=True)
    vegan = models.BooleanField(null=True)
    allergens = models.BooleanField(null=True)
    lactose_free = models.BooleanField(null=True)
    sugarless = models.BooleanField(null=True)
    gluten_free = models.BooleanField(null=True)
    description = models.CharField(max_length=1000, null=True)
    ovd = models.BooleanField(null=True)
    ovd_sugarless = models.BooleanField(null=True)
    shd = models.BooleanField(null=True)
    bd = models.BooleanField(null=True)
    vbd = models.BooleanField(null=True)
    nbd = models.BooleanField(null=True)
    nkd = models.BooleanField(null=True)
    vkd = models.BooleanField(null=True)
    not_suitable = models.BooleanField(null=True)
    category = models.CharField(max_length=2000, null=True)
    cooking_method = models.CharField(max_length=7000, null=True)
    comment = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return f'{self.name}, {self.category}'


class Timetable(models.Model):
    datetime = models.DateField()
    item = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    date_create = models.DateField(default=date.today, null=True)
    def __str__(self):
        return f'{self.item}'


class MenuByDay(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    meal = models.CharField(
            max_length=100,
            choices=MEALS,
            blank=True,
            default='',
        )
    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')
    main = models.CharField(max_length=100, null=True)
    garnish = models.CharField(max_length=100, null=True)
    porridge = models.CharField(max_length=100, null=True)
    soup = models.CharField(max_length=100, null=True)
    dessert = models.CharField(max_length=100, null=True)
    fruit = models.CharField(max_length=100, null=True)
    drink = models.CharField(max_length=100, null=True)
    salad = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user_id} {self.date}'

class UsersReadyOrder(models.Model):
    user_id = models.CharField(max_length=200, null=True)
    date_create = models.DateField(default=date.today)
    full_name = models.CharField(max_length=200, null=True)
    receipt_date = models.DateField(null=True)
    receipt_time = models.TimeField(null=True)

    department = models.CharField(
        max_length=100,
        choices=TYPE_DEPARTMENT,
        blank=True,
        default='Не выбрано',
        help_text='Выбор отделения')

    room_number = models.CharField(
        max_length=100,
        choices=ROOM_NUMBERS,
        blank=True,
        default='200',
        help_text='Выбор номера палаты')

    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')

    comment = models.CharField(
        max_length=1000,
        null=True,
        blank=True)

    status = models.CharField(
        max_length=100,
        choices=STATUS_PATIENT,
        blank=True,
        default='',
        help_text='Выбор диеты')


    def __str__(self):
        return f'{self.full_name}'


class MenuByDayReadyOrder(models.Model):
    user_id = models.ForeignKey('UsersReadyOrder', on_delete=models.CASCADE, null=True)
    date_create = models.DateField(default=date.today)
    date = models.DateField()
    meal = models.CharField(
            max_length=100,
            choices=MEALS,
            blank=True,
            default='',
        )
    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')
    main = models.CharField(max_length=100, null=True)
    garnish = models.CharField(max_length=100, null=True)
    porridge = models.CharField(max_length=100, null=True)
    soup = models.CharField(max_length=100, null=True)
    dessert = models.CharField(max_length=100, null=True)
    fruit = models.CharField(max_length=100, null=True)
    drink = models.CharField(max_length=100, null=True)
    salad = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user_id} {self.date}'


class ProductLp(models.Model):
    name = models.CharField(max_length=200, null=True)
    carbohydrate = models.CharField(max_length=200, null=True)
    fat = models.CharField(max_length=200, null=True)
    fiber = models.CharField(max_length=200, null=True)
    energy = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=2000, null=True)
    description = models.CharField(max_length=1000, null=True)
    category = models.CharField(max_length=2000, null=True)
    comment = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return f'{self.name}, {self.category}'

class TimetableLp(models.Model):
    item = models.ForeignKey('ProductLp', on_delete=models.SET_NULL, null=True)
    day_of_the_week = models.CharField(
        max_length=100,
        choices=DAT_OF_THE_WEEK,
        blank=True,
        default='',
        help_text='День недели')
    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='',
        help_text='Выбор диеты')
    meals = models.CharField(
        max_length=100,
        choices=MEALS,
        blank=True,
        default='',
        help_text='Выбор диеты')
    def __str__(self):
        return f'{self.item}'


class Barcodes(models.Model):
    number = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUS_BARCODES,
        default='active',
       )
    def __str__(self):
        return f'{self.number}'

class CommentProduct(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    product_id = models.CharField(max_length=200, null=True)
    date_create = models.DateField(default=datetime.now)
    comment = models.CharField(
        max_length=10000,
        null=True,
        blank=True)
    rating = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.user_id} {self.product_id}'


class BotChatId(models.Model):
    chat_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.chat_id}'


class Report(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    product_id = models.CharField(max_length=200, null=True)
    date_create = models.DateField(default=date.today)
    meal = models.CharField(
            max_length=100,
            choices=MEALS,
            blank=True,
            default='',
        )
    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        default='ОВД',
        help_text='Выбор диеты')

    def __str__(self):
        return f'{self.user_id} {self.date_create} {self.meal}'