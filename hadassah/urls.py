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



urlpatterns = [
    path('admin/', admin.site.urls),
    path('nutritionist/', include('nutritionist.urls')),
    path('', views.redirect, name='redirect'),
    path('api/v1/auth/', include('djoser.urls')),
    # re_path('auth/', include('djoser.urls.authtoken')),
    path('api/v1/baselist/', BaseAPIView.as_view()),
    path('accounts/login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='reset_password'),
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
