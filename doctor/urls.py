from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('', views.doctor, name='doctor'),
    path('archive', views.archive, name='archive'),
    path('menu', views.menu, name='menu'),
    path('admin', views.admin, name='admin'),
    path('test', views.test, name='test'),
    path('printed_form_one', views.printed_form_one, name='printed_form_one'),
    path('printed_form_two_lp', views.printed_form_two_lp, name='printed_form_two'),
    path('printed_form_two_cafe', views.printed_form_two_cafe, name='printed_form_cafe'),
    path('api/v1/password/verify', views.VerifyPasswordAPIView.as_view()),
    path('api/v1/patient/menu', views.GetPatientMenuAPIView.as_view()),
    path('api/v1/patient/menu/day', views.GetPatientMenuDayAPIView.as_view()),
    ]

