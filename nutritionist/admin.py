# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Base, Product, Timetable, CustomUser, ProductLp, TimetableLp


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
    list_display = ('name', 'category', 'description',)
    fields = ('name', 'category', 'description',)
    list_per_page = 200

    inlines = [TimetableLpAdmin]

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # fields = ['full_name', 'comment', 'email', 'username']
    list_display = ['username', 'email', 'full_name', 'comment']

admin.site.register(CustomUser, CustomUserAdmin)