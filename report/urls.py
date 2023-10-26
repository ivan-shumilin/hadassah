from django.urls import path, re_path, include
from . import views
app_name = 'report'

urlpatterns = [
    path('dish_assembly_report', views.dish_assembly_report, name='dish_assembly_report'),
    ]

