from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('<id>', views.patient, name='patient'),
    path('history/<id>', views.patient_history, name='patient_history'),
    path('history/test/test', views.patient_history_test, name='patient_history_test'),
    path('api/v1/submitselection', views.SubmitPatientSelectionAPIView.as_view()),
    ]

