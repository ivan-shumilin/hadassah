"""hadassah URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from nutritionist.views import *
from nutritionist import views
from doctor.views import menu_for_staff



urlpatterns = [
    path('admin/', admin.site.urls),
    path('nutritionist/', include('nutritionist.urls')),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
    path('', views.redirect, name='redirect'),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/baselist/', BaseAPIView.as_view()),
    path('api/v1/barcode/verify', VerifyAPIView.as_view()),
    path('api/v1/barcode/deactivate', DeactivateAPIView.as_view()),
    path('login/', views.user_login, name='login'),
    path('report/', views.report, name='report'),
    path('manager/report/', views.reports, name='reports'),
    path('menu/', menu_for_staff, name='menu_for_staff'),
    path('manager/', views.manager, name='manager'),
    path('manager/printed_form_one', views.printed_form_one, name='printed_form_one'),
    path('manager/printed_form_two_lp', views.printed_form_two_lp, name='printed_form_two'),
    path('manager/printed_form_two_cafe', views.printed_form_two_cafe, name='printed_form_cafe'),
    path('manager/menu', views.menu_lp_for_staff, name='menu_lp_for_staff'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
    path('report/api/v1/get/downloadreport', views.DownloadReportAPIView.as_view()),
    path('manager/api/v1/get/downloadsstickers', views.CreateSitckers.as_view()),
]



