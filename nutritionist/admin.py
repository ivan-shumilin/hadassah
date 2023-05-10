# users/admin.py
import random

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Base, Product, Timetable, CustomUser, ProductLp, TimetableLp, MenuByDay, Barcodes, CommentProduct, \
    BotChatId, UsersToday, СhangesUsersToday, UsersReadyOrder, MenuByDayReadyOrder, Report, ProductStorage, Ingredient, \
    ModifiedDish

admin.site.register(Base)

class TimetableAdmin(admin.ModelAdmin):
    list_display = ('item', 'datetime',)
    list_filter = ('datetime',)
    list_per_page = 600

class TimetableLpAdmin(admin.ModelAdmin):
    list_display = ('item', 'day_of_the_week', 'type_of_diet', 'meals',)
    fields = ('item', 'day_of_the_week', 'type_of_diet', 'meals',)
    list_per_page = 600

admin.site.register(Timetable, TimetableAdmin)
admin.site.register(TimetableLp, TimetableLpAdmin)

class TimetableLpAdmin(admin.TabularInline):
    model = TimetableLp
    list_per_page = 600

class TimetableAdmin(admin.TabularInline):
    model = Timetable
    list_per_page = 600

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'public_name', 'iditem', 'with_garnish', 'ovd', 'ovd_vegan', 'ovd_sugarless', 'shd',
                    'shd_sugarless', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category', 'iodine_free',)
    fields = ('name', 'public_name', 'iditem', 'with_garnish', 'ovd', 'ovd_vegan', 'ovd_sugarless',\
              'shd', 'shd_sugarless', 'iodine_free', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category', 'description',)
    list_filter = ('category', 'with_garnish', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd',)
    list_per_page = 500

    inlines = [TimetableAdmin]

@admin.register(ProductLp)
class ProductLpAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_id', 'public_name', 'with_garnish', 'category', 'description', 'status')
    fields = ('name', 'public_name', 'image', 'preview', 'edit_photo', 'product_id', 'with_garnish', 'number_tk', 'category', 'carbohydrate', 'fat', 'fiber',
              'energy', 'weight', 'description', 'comment', 'status')
    list_filter = ('category', 'status',)
    list_per_page = 1000
    readonly_fields = ["preview", "edit_photo"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}?v={str(random.randint(1, 1000))}" style="max-height: 150px;">')

    def edit_photo(self, obj):
        link = reverse('edit_photo', args=[obj.pk])
        return mark_safe(f'<a href="{link}" style="max-height: 200px; font-weight: 600;">Редактировать фото блюда</a>')

    def save_model(self, request, obj, form, change):
        # Получаем объект файла из формы
        image = form.cleaned_data['image']

        # Генерируем новое имя файла, например, на основе текущего времени
        new_filename = f"{obj.pk}.{image.name.split('.')[-1]}"

        # Сохраняем файл с новым именем
        obj.image.save(new_filename, image)

        # Вызываем родительский метод для сохранения объекта модели
        super().save_model(request, obj, form, change)

    inlines = [TimetableLpAdmin]

@admin.register(CommentProduct)
class CommentProductAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'date_create', 'comment', 'rating',)
    fields = ('user_id', 'product_id', 'date_create', 'comment', 'rating',)
    list_per_page = 600

@admin.register(MenuByDay)
class MenuByDayAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'meal', 'type_of_diet')
    fields = ('user_id', 'date', 'type_of_diet', 'meal', 'main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit',
              'drink', 'salad', 'products', 'hidden', 'bouillon')
    list_per_page = 600

@admin.register(UsersToday)
class UsersTodayAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    fields = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    list_per_page = 600

@admin.register(СhangesUsersToday)
class СhangesUsersTodayAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'receipt_date', 'type_of_diet', 'room_number', 'status')
    fields = ('full_name', 'receipt_date', 'type_of_diet', 'room_number', 'status')
    list_per_page = 600

@admin.register(Barcodes)
class BarcodesAdmin(admin.ModelAdmin):
    list_display = ('number', 'status')
    fields = ('number', 'status')
    list_per_page = 600

@admin.register(BotChatId)
class BotChatIdAdmin(admin.ModelAdmin):
    list_display = ('chat_id',)
    fields = ('chat_id',)
    list_per_page = 600



@admin.register(MenuByDayReadyOrder)
class MenuByDayReadyOrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'meal')
    fields = ('user_id', 'date', 'meal', 'main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit', 'drink', 'salad',
              'products', 'bouillon')
    list_per_page = 600


@admin.register(UsersReadyOrder)
class UsersReadyOrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    fields = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    list_per_page = 600


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'date_create', 'meal', 'type_of_diet')
    fields = ('user_id', 'product_id', 'date_create', 'meal', 'type_of_diet')
    list_per_page = 600

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'product_id',)
    fields = ('name', 'code', 'product_id',)
    list_per_page = 1000

@admin.register(ProductStorage)
class ProductStorageAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'meal', 'category', 'products_id')
    fields = ('date_create', 'meal', 'category', 'products_id')
    list_per_page = 600

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # fields = ['full_name', 'comment', 'email', 'username']
    list_display = ['username', 'email', 'full_name', 'comment']

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(ModifiedDish)
class ModifiedDishAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'date', 'meal', 'user_id')
    fields = ('product_id', 'date', 'meal', 'user_id')
    list_per_page = 600