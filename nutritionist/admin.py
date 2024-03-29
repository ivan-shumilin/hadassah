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
    ModifiedDish, TTK, AllProductСache, IngredientСache

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
    list_display = ('name', 'public_name', 'with_garnish', 'ovd', 'ovd_vegan', 'ovd_sugarless', 'shd',
                    'shd_sugarless', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category', 'iodine_free',)
    fields = ('name', 'public_name', 'iditem', 'with_garnish', 'ovd', 'ovd_vegan', 'ovd_sugarless',\
              'shd', 'shd_sugarless', 'iodine_free', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category', 'description',)
    list_filter = ('category', 'with_garnish', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd',)
    list_per_page = 500

    inlines = [TimetableAdmin]

@admin.register(ProductLp)
class ProductLpAdmin(admin.ModelAdmin):
    list_display = ('name', 'public_name', 'with_phote', 'with_garnish', 'category', 'description', 'status', 'product_id')
    fields = ('name', 'public_name', 'primary_key', 'image', 'preview', 'edit_photo', 'preview_min', 'edit_photo_min', 'product_id', 'with_garnish', 'number_tk', 'category', 'carbohydrate', 'fat', 'fiber',
              'energy', 'weight', 'description', 'comment', 'status')
    list_filter = ('with_phote', 'category')
    list_per_page = 1000
    readonly_fields = ["preview", "preview_min", "edit_photo", "edit_photo_min", "primary_key"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}?v={str(random.randint(1, 1000))}" style="max-height: 150px;">')
    preview.short_description = 'Превью основного фото'

    def preview_min(self, obj):
        return mark_safe(f'<img src="{obj.image_min.url}?v={str(random.randint(1, 1000))}" style="max-height: 150px;">')
    preview_min.short_description = 'Превью миниатюры'

    def edit_photo(self, obj):
        link = reverse('edit_photo', args=[obj.pk, 'full'])
        return mark_safe(f'<a href="{link}" style="max-height: 200px; font-weight: 600;">Кадрировать основное фото</a>')
    edit_photo.short_description = 'Редактировать'

    def edit_photo_min(self, obj):
        link = reverse('edit_photo', args=[obj.pk, 'min'])
        return mark_safe(f'<a href="{link}" style="max-height: 200px; font-weight: 600;">Кадрировать миниатюру</a>')
    edit_photo_min.short_description = 'Редактировать'

    def primary_key(self, obj):
        return obj.pk
    primary_key.short_description = 'Primary key'

    def save_model(self, request, obj, form, change):

        # Получаем объект файла из формы
        image = form.cleaned_data['image']

        try:
            #Проверяем изменилось ли фото
            if obj.image.file != image.file:
                image_min = form.cleaned_data['image']

                # Генерируем новое имя файла
                if hasattr(image, 'name'):
                    new_filename = f"{obj.pk}.{image.name.split('.')[-1]}"

                    # Сохраняем файл с новым именем
                    obj.image.save(new_filename, image)

                    new_filename = f"{obj.pk}.{image.name.split('.')[-1]}"

                    # Сохраняем файл с новым именем
                    obj.image_min.save(new_filename, image_min)
                    obj.with_phote = True

        except ValueError:
            obj.image_min.delete()  # удаляем старое изображение
            obj.with_phote = False

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
    fields = ('user_id', 'product_id', 'date_create', 'meal', 'type_of_diet', 'type')
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
    list_display = ('product_id', 'date', 'meal', 'user_id', 'status')
    fields = ('product_id', 'date', 'meal', 'user_id', 'status')
    list_per_page = 600


@admin.register(TTK)
class TTKAdmin(admin.ModelAdmin):
    list_display = ('measure_unit', 'product_id', 'name', 'create_at', 'parent_ttk', 'amount_in', 'amount_middle', 'amount_out', 'ingredient', 'status')
    fields = ('measure_unit', 'product_id', 'name', 'create_at', 'parent_ttk', 'amount_in', 'amount_middle', 'amount_out', 'ingredient', 'status')
    list_per_page = 600


@admin.register(AllProductСache)
class AllProductСacheAdmin(admin.ModelAdmin):
    pass
    # list_display = ('date_create', 'meal', 'category', 'products_id')
    # fields = ('date_create', 'meal', 'category', 'products_id')
    # list_per_page = 600


@admin.register(IngredientСache)
class IngredientСacheAdmin(admin.ModelAdmin):
    pass