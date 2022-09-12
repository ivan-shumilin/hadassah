from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('<id>', views.patient, name='patient'),
    path('test/', views.test, name='test'),
    ]