from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularSwaggerView

from hadassah import settings
from nutritionist.views import *
from nutritionist import views
from hadassah.spectacular.urls import urlpatterns as doc_urls

handler403 = 'doctor.views.tr_handler403'
handler404 = 'doctor.views.tr_handler404'
handler500 = 'doctor.views.tr_handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', login_required(SpectacularSwaggerView.as_view(url_name="schema")), name="swagger-ui"),
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
    path('internal-report/', views.internal_report, name='internal_report'), # для отдельной учетки
    # path('menu/', menu_for_staff, name='menu_for_staff'),
    path('manager/', views.manager, name='manager'),
    path('manager/detailing/<meal>', views.detailing, name='detailing'),
    path('manager/detailing_reports/<meal>/<floor>', views.detailing_reports, name='detailing_reports'),
    path('manager/printed_form_one', views.printed_form_one, name='printed_form_one'),
    path('manager/printed_form_one_new', views.printed_form_one_new, name='printed_form_one_new'),
    path('manager/brakery_magazine', views.brakery_magazine, name='brakery_magazine'),
    path('manager/printed_form_two_lp', views.printed_form_two_lp, name='printed_form_two'),
    path('manager/printed_form_two_lp_new', views.printed_form_two_lp_new, name='printed_form_two_lp_new'),
    path('manager/printed_form_two_cafe', views.printed_form_two_cafe, name='printed_form_cafe'),
    path('manager/printed_form_two_cafe_new', views.printed_form_two_cafe_new, name='printed_form_cafe_new'),
    path('manager/tk/<id>/<count>', views.tk, name='tk'),
    path('manager/tk_for_cafe/<id>/<count>', views.tk, name='tk_for_cafe'),
    path('manager/tk_for_cafe_alcon/<id>/<count>', views.tk, name='tk_for_cafe_alkon'),
    path('manager/tk_for_cafe_renova/<id>/<count>', views.tk, name='tk_for_cafe_renova'),
    path('hadassah/ttk-tool/', views.product_storage_hadassah, name='product_storage_hadassah'),
    path('alcon/ttk-tool/', views.product_storage_alcon, name='product_storage_alcon'),
    path('renova/ttk-tool/', views.product_storage_renova, name='product_storage_renova'),
    path('start_page_product_storage/', views.start_page_product_storage, name='start_page_product_storage'),
    path('manager/without_menu/for_epidemiologist/tk/<id>/<count>', views.tk, name='tk_for_epidemiologist'),
    path('manager/admin-foods/', views.admin_foods, name='admin_foods'),
    path('manager/admin-foods-new/', views.admin_foods_new, name='admin_foods_new'),
    path('manager/edit-photo/<product_id>/<type>', views.edit_photo, name='edit_photo'),
    path('manager/photo_statistics', views.photo_statistics, name='photo_statistics'),
    path('manager/menu', views.menu_lp_for_staff, name='menu_lp_for_staff'),
    path('manager/without_menu/for_epidemiologist', views.menu_lp_for_staff, name='menu_lp_for_staff_without_report'),
    path('manager/order', views.all_order_by_ingredients, name='order'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
    path('api/v1/get/downloadreport', views.DownloadReportAPIView.as_view()),
    path('api/v1/get/check-is-report', views.CheckIsReportAPIView.as_view()),
    path('api/v1/get/download_brakery', views.DownloadBrakeryAPIView.as_view()),
    path('api/v1/get/check-is-brakery', views.CheckIsBrakeryAPIView.as_view()),
    path('api/v1/get_all_dishes_from_iiko', views.FetchAllProductsFromIIKOAPIView.as_view()),
    path('api/v1/get_products_for_product_storage', views.get_all_product),
    path('manager/api/v1/get/downloadsstickers', views.CreateStickers.as_view(), name='create_stickers'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
