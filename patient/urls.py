from django.urls import path, re_path, include
from . import views
app_name = 'patient'

urlpatterns = [
    path('', views.user_login, name='patient-login'),
    path('history/<id>', views.patient_history, name='patient_history'),
    path('history/test/test', views.patient_history_test, name='patient_history_test'),
    path('<id>', views.patient, name='patient'),
    path('api/v1/submitselection', views.SubmitPatientSelectionAPIView.as_view()),
    path('api/v1/login/datavalidation', views.loginDataValidationAPIView.as_view())
    ]

