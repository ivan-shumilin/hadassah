from django.db import models
from datetime import date
from datetime import datetime
import uuid
from django.contrib.auth.models import AbstractUser
from doctor.choices import *
from patient.choices import *


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200, null=True)
    birthdate = models.DateField(null=True)  # datetime.date
    receipt_date = models.DateField(null=True)  # datetime.date
    receipt_time = models.TimeField(null=True)  # datetime.time
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

    is_accompanying =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Cопровождающий?')

    is_probe =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Питание через зонд')

    is_without_salt = models.BooleanField(
        blank=True,
        default=False,
        help_text='Без соли')

    is_without_lactose = models.BooleanField(
        blank=True,
        default=False,
        help_text='Без лактозы')

    is_pureed_nutrition = models.BooleanField(
        blank=True,
        default=False,
        help_text='Протертое питание')

    type_pay = models.CharField(
        max_length=100,
        choices=TYPE_PAY,
        blank=True,
        default='',
        help_text='Тип оплаты')

    is_change_diet_bd = models.BooleanField(
        blank=True,
        default=True,
        help_text='Чередовать диету БД при следующей смене? (19:00)')

    # если есть доп. бульон, тогда будут указаны приемы пищи через запятую
    extra_bouillon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default='',
        help_text='Дополнительный бульон')

    def __str__(self):
        return f'{self.full_name}, {self.type_of_diet}, {self.is_change_diet_bd}'

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

    is_accompanying =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Cопровождающий?')

    is_probe =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Питание через зонд')

    is_without_salt =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Без соли')

    is_without_lactose =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Без лактозы')

    is_pureed_nutrition = models.BooleanField(
        blank=True,
        default=False,
        help_text='Протертое питание')

    type_pay = models.CharField(
        max_length=100,
        choices=TYPE_PAY,
        blank=True,
        default='',
        help_text='Тип оплаты')


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
    date_create = models.DateField(default=date.today, null=True, blank=True)
    iditem = models.IntegerField(null=True)
    public_name = models.CharField(max_length=200, null=True, blank=True)
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
    with_garnish =   models.BooleanField(
        blank=True,
        default=False,
        help_text='Блюдо уже с гарниром?')

    def __str__(self):
        return f'{self.name}, {self.category}'


class Timetable(models.Model):
    datetime = models.DateField()
    item = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    date_create = models.DateField(default=date.today, null=True)
    def __str__(self):
        return f'{self.item}'


class MenuByDay(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
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
    main = models.CharField(max_length=100, null=True, blank=True)
    garnish = models.CharField(max_length=100, null=True, blank=True)
    porridge = models.CharField(max_length=100, null=True, blank=True)
    soup = models.CharField(max_length=100, null=True, blank=True)
    dessert = models.CharField(max_length=100, null=True, blank=True)
    fruit = models.CharField(max_length=100, null=True, blank=True)
    drink = models.CharField(max_length=100, null=True, blank=True)
    salad = models.CharField(max_length=100, null=True, blank=True)
    products = models.CharField(max_length=100, null=True, blank=True)
    hidden = models.CharField(max_length=100, null=True, blank=True)
    bouillon = models.CharField(max_length=100, null=True, blank=True)

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
    is_accompanying = models.BooleanField(
        blank=True,
        default=False,
        help_text='Cопровождающий?')

    is_probe =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Питание через зонд')

    is_without_salt =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Без соли')

    is_without_lactose =  models.BooleanField(
        blank=True,
        default=False,
        help_text='Без лактозы')

    is_pureed_nutrition = models.BooleanField(
        blank=True,
        default=False,
        help_text='Протертое питание')

    type_pay = models.CharField(
        max_length=100,
        choices=TYPE_PAY,
        blank=True,
        default='',
        help_text='Тип оплаты')


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
    products = models.CharField(max_length=100, null=True)
    bouillon = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user_id} {self.date}'


class ProductLp(models.Model):
    name = models.CharField(max_length=200, null=True)
    public_name = models.CharField(max_length=200, null=True, blank=True)
    carbohydrate = models.CharField(max_length=200, null=True, blank=True)
    fat = models.CharField(max_length=200, null=True, blank=True)
    fiber = models.CharField(max_length=200, null=True, blank=True)
    energy = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=2000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    category = models.CharField(max_length=2000, null=True, blank=True)
    comment = models.CharField(max_length=5000, null=True, blank=True)
    weight = models.CharField(max_length=5000, null=True, blank=True)
    number_tk = models.CharField(max_length=5000, null=True, blank=True)
    # у новых блюд статус равен 1
    status = models.CharField(max_length=500, null=True, default='1',)
    with_garnish =   models.BooleanField(
        blank=True,
        default=False,
        help_text='Блюдо уже с гарниром?')

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


class ProductStorage(models.Model):
    """
    Таблица для вывода данных в "Заявку по блюдам линии раздачи"
    Блюда, которые уже пошли в производство и не будут меняться.
    """
    date_create = models.DateField(default=date.today)
    type_of_diet = models.CharField(
        max_length=100,
        choices=TYPE_DIET,
        blank=True,
        help_text='Тип диеты')
    meal = models.CharField(
            max_length=100,
            choices=MEALS,
            blank=True,
            default='',
        )
    category = models.CharField(max_length=200, null=True, blank=True)
    products_id =models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.date_create} {self.meal} {self.category} {self.products_id}'