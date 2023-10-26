from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include, re_path

from hadassah import settings
from nutritionist.views import *
from nutritionist import views
from hadassah.spectacular.urls import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('nutritionist/', include('nutritionist.urls')),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
    path('report/', include('report.urls')),
    path('', views.redirect, name='redirect'),
    # path('', include('pwa.urls')),
    # path('nutritionist/', include('pwa.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('sw.js',
         views.ServiceWorkerView.as_view(),
         name=views.ServiceWorkerView.name,
         ),
    path('api/v1/baselist/', BaseAPIView.as_view()),
    path('api/v1/barcode/verify', VerifyAPIView.as_view()),
    path('api/v1/barcode/deactivate', DeactivateAPIView.as_view()),
    path('login/', views.user_login, name='login'),
    path('report/', views.report, name='report'),
    # path('manager/report/', views.reports, name='reports'),
    path('internal-report/', views.internal_report, name='internal_report'),
    # path('menu/', menu_for_staff, name='menu_for_staff'),
    path('manager/', views.manager, name='manager'),
    path('manager/printed_form_one', views.printed_form_one, name='printed_form_one'),
    path('manager/printed_form_one_new', views.printed_form_one_new, name='printed_form_one_new'),
    path('manager/printed_form_two_lp', views.printed_form_two_lp, name='printed_form_two'),
    path('manager/printed_form_two_lp_new', views.printed_form_two_lp_new, name='printed_form_two_lp_new'),
    path('manager/printed_form_two_cafe', views.printed_form_two_cafe, name='printed_form_cafe'),
    path('manager/printed_form_two_cafe_new', views.printed_form_two_cafe_new, name='printed_form_cafe_new'),
    path('manager/tk/<id>/<count>', views.tk, name='tk'),
    path('manager/admin-foods/', views.admin_foods, name='admin_foods'),
    path('manager/admin-foods-new/', views.admin_foods_new, name='admin_foods_new'),
    path('manager/edit-photo/<product_id>/<type>', views.edit_photo, name='edit_photo'),
    path('manager/photo_statistics', views.photo_statistics, name='photo_statistics'),
    path('manager/menu', views.menu_lp_for_staff, name='menu_lp_for_staff'),
    path('manager/order', views.all_order_by_ingredients, name='order'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
    path('api/v1/get/downloadreport', views.DownloadReportAPIView.as_view()),
    path('api/v1/get/check-is-report', views.CheckIsReportAPIView.as_view()),
    path('manager/api/v1/get/downloadsstickers', views.CreateStickers.as_view(), name='create_stickers'),
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


urlpatterns += doc_urls

