from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('', views.doctor, name='doctor'),
    path('archive', views.archive, name='archive'),
    path('menu', views.menu, name='menu'),
    path('api/v1/password/verify', views.VerifyPasswordAPIView.as_view()),
    path('api/v1/get/occupiedrooms', views.GetOccupiedRoomsAPIView.as_view()),
    path('api/v1/patient/menu', views.GetPatientMenuAPIView.as_view()),
    path('api/v1/patient/menu/day', views.GetPatientMenuDayAPIView.as_view()),
    ]

