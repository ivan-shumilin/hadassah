from django.urls import path, re_path, include
from . import views
from .api import PatientDetail, PatientHistory, PatientMenuDetail, PatientLoginAPI, ProtectedView, RefreshTokenAPI

app_name = 'patient'

urlpatterns = [
    path('', views.user_login, name='patient-login'),
    path('history/<id>', views.patient_history, name='patient_history'),
    path('history/test/test', views.patient_history_test, name='patient_history_test'),
    path('<id>', views.patient, name='patient'),
    path('api/v1/submitselection', views.SubmitPatientSelectionAPIView.as_view()),
    path('api/v1/login/datavalidation', views.loginDataValidationAPIView.as_view()),
    path('logout/', views.patient_logout, name='patient_logout'),
    ]

api_urlpatterns = [
    path('api/v1/patient-login/', PatientLoginAPI.as_view(), name='api-patient-login'),
    path('api/v1/token/refresh/', RefreshTokenAPI.as_view(), name='api-refresh-token'),
    path('api/v1/patient-info/<int:user_id>/', PatientDetail.as_view(), name='api-patient-detail'),
    path('api/v1/patient-history/<int:user_id>/', PatientHistory.as_view(), name='api-patient-history'),
    path('api/v1/patient-menu/<int:user_id>/', PatientMenuDetail.as_view(), name='api-patient-menu'),

    # path('api/v1/protected/', ProtectedView.as_view(), name='protected'), # - тест JWT
]

urlpatterns += api_urlpatterns
