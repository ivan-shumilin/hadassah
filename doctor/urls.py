from django.urls import path
from . import views


urlpatterns = [
    path('', views.doctor, name='doctor'),
    path('archive', views.archive, name='archive'),
    path('menu', views.menu, name='menu'),
    # path('menu-guest', views.menu_for_staff, name='menu_for_staff'),
    path('api/v1/password/verify', views.VerifyPasswordAPIView.as_view()),
    path('api/v1/get/occupiedrooms', views.GetOccupiedRoomsAPIView.as_view()),
    path('api/v1/patient/menu', views.GetPatientMenuAPIView.as_view()),
    path('api/v1/patient/menu/day', views.GetPatientMenuDayAPIView.as_view()),
    path('api/v1/get-all-dishes-by-category', views.GetAllDishesByCategoryAPIView.as_view()),
    path('api/v1/delete-dish', views.DeleteDishAPIView.as_view()),
    path('api/v1/add-dish', views.AddDishAPIView.as_view()),
    path('api/v1/change-dish', views.ChangeDishAPIView.as_view()),
    path('api/v1/get-patients', views.GetPatientsAPIView.as_view()),
    path('api/v1/get-info-patient', views.GetInfoPatientAPIView.as_view()),
    path('api/v1/menu-patient-one-day', views.GetPatientMenuDayTestAPIView.as_view()),
    path('api/v1/send_emergency_food', views.SendEmergencyFoodAPIView.as_view()),
    path('api/v1/send-patient-products', views.SendPatientProductsAPIView.as_view()),
    path('api/v1/update-search', views.UpdateSearchAPIView.as_view()),
    path('api/v1/cropp_image', views.CroppImageAPIView.as_view()),
]