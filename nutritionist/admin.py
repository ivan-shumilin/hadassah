# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Base, Product, Timetable, CustomUser, ProductLp, TimetableLp, MenuByDay, Barcodes, CommentProduct, \
    BotChatId, UsersToday, СhangesUsersToday, UsersReadyOrder, MenuByDayReadyOrder, Report


admin.site.register(Base)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cooking_method', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category',)
    fields = ('name', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category', 'description',)
    list_filter = ('category', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'description',)
    # list_filter = ('status', 'due_back')

# class ProductLpAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category',)
#     fields = ('name', 'category', 'description',)


class TimetableAdmin(admin.ModelAdmin):
    list_display = ('item', 'datetime',)
    list_filter = ('datetime',)

class TimetableLpAdmin(admin.ModelAdmin):
    list_display = ('item', 'day_of_the_week', 'type_of_diet', 'meals',)
    fields = ('item', 'day_of_the_week', 'type_of_diet', 'meals',)



admin.site.register(Timetable, TimetableAdmin)
admin.site.register(TimetableLp, TimetableLpAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductLp, ProductLpAdmin)

class TimetableLpAdmin(admin.TabularInline):
    model = TimetableLp

@admin.register(ProductLp)
class ProductLpAdmin(admin.ModelAdmin):
    list_display = ('name', 'public_name', 'category', 'description',)
    fields = ('name', 'public_name', 'category', 'carbohydrate', 'fat', 'fiber', 'energy', 'weight', 'description', 'comment',)
    list_filter = ('category', 'carbohydrate', 'fat', 'fiber', 'energy', 'weight', 'description', 'status',)
    list_per_page = 500

    inlines = [TimetableLpAdmin]

@admin.register(CommentProduct)
class CommentProductAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'date_create', 'comment', 'rating',)
    fields = ('user_id', 'product_id', 'date_create', 'comment', 'rating',)
    list_per_page = 200

@admin.register(MenuByDay)
class MenuByDayAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'meal', 'type_of_diet')
    fields = ('user_id', 'date', 'type_of_diet', 'meal', 'main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit', 'drink', 'salad')
    list_per_page = 200

@admin.register(UsersToday)
class UsersTodayAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    fields = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    list_per_page = 200

@admin.register(СhangesUsersToday)
class СhangesUsersTodayAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'receipt_date', 'type_of_diet', 'room_number', 'status')
    fields = ('full_name', 'receipt_date', 'type_of_diet', 'room_number', 'status')
    list_per_page = 200

@admin.register(Barcodes)
class BarcodesAdmin(admin.ModelAdmin):
    list_display = ('number', 'status')
    fields = ('number', 'status')
    list_per_page = 200

@admin.register(BotChatId)
class BotChatIdAdmin(admin.ModelAdmin):
    list_display = ('chat_id',)
    fields = ('chat_id',)
    list_per_page = 200



@admin.register(MenuByDayReadyOrder)
class MenuByDayReadyOrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'meal')
    fields = ('user_id', 'date', 'meal', 'main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit', 'drink', 'salad')
    list_per_page = 200


@admin.register(UsersReadyOrder)
class UsersReadyOrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    fields = ('full_name', 'receipt_date', 'receipt_time', 'type_of_diet', 'status')
    list_per_page = 200


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'date_create', 'meal', 'type_of_diet')
    fields = ('user_id', 'product_id', 'date_create', 'meal', 'type_of_diet')
    list_per_page = 500



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # fields = ['full_name', 'comment', 'email', 'username']
    list_display = ['username', 'email', 'full_name', 'comment']

admin.site.register(CustomUser, CustomUserAdmin)