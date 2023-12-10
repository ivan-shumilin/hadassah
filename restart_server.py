# ssh shumilin@158.160.15.85
# ssh shumilin@130.193.55.25
# nohup python3 manage.py runapscheduler &
# python3 manage.py runapscheduler
#  690838
"""
chat id для основного сервера:
1. 	369027587
1. -1001862610966
dev:
1. -1001857872715
"""
"""
coverage run --source='.' ./manage.py test .
coverage report
coverage html
"""
# from datetime import date

"""
restart() {
sudo supervisorctl restart hadassah
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx

}

"""
"""
Leslie William Nielsen
"""
"""
настройка конфига celery 
sudo nano /etc/supervisor/conf.d/hadassah.conf
"""
"""
CHAT ID
-1001862610966
"""

""""
логин: sk.hadassah2023@gmail.com
пароль: Skolkovo2023
"""

"""
celery -A hadassah worker
sudo nano /var/log/supervisor/test.out.log
sudo nano /var/log/supervisor/test.err.log
"""

"""
gonicorn - проверка логов
sudo tail -f /var/log/syslog
"""

"""
backup

Product.objects.all().delete()
ProductLp.objects.all().delete()
Timetable.objects.all().delete()
TimetableLp.objects.all().delete()
MenuByDay.objects.all().delete()
MenuByDayReadyOrder.objects.all().delete()
UsersReadyOrder.objects.all().delete()
UsersToday.objects.all().delete()
CustomUser.objects.all().delete()

"""

# добавить приложение новое в проект
# 1. """./manage.py startapp report"""
# 2. """nano hadassah/settings.py"""
"""
INSTALLED_APPS = [
    ...
    'report',
    ...
]
"""

# Как скопировать диеты из ОВД в ОВД (Э)

# create_user_today() # создаем таблицу с пользователями на сегодня
# my_job_create_ready_order_dinner.delay()

not_active_users_set = get_not_active_users_set()

from nutritionist.models import CustomUser, Product, Timetable, ProductLp, MenuByDay, BotChatId, СhangesUsersToday, UsersToday, TimetableLp
from doctor.functions.for_print_forms import create_user_today, create_ready_order, create_report
from doctor.functions.diet_formation import add_default_menu_on_one_day, add_menu_three_days_ahead


MenuByDay.objects.filter(date='2023-06-08').delete()
MenuByDay.objects.filter(date='2023-06-09').delete()
MenuByDay.objects.filter(date='2023-06-10').delete()
add_menu_three_days_ahead()
create_user_today('tomorrow')

create_ready_order('breakfast')
create_ready_order('lunch')
create_ready_order('afternoon')
create_ready_order('dinner')
create_user_today('breakfast')
# create_user_today('lunch')
# create_user_today('afternoon')
# create_user_today('dinner')
# create_user_today('tomorrow')

create_report('breakfast')
create_report('afternoon')

# Обновление ingredients
# from doctor.logic.create_ingredient import create_ingredients
# create_ingredients()
#
#
# # from doctor.logic.create_ingredient import create_ingredients
# from doctor.functions.download import get_token, get_tk
# from nutritionist.functions.descripton_parsing import description_parsing
# products = Product.objects.filter(category='Завтраки').filter(description='Отсутствует')
#
#
# for product in products:
#     product.description = description_parsing(product.product_id)
#     product.save()
#
# id="946126a9-f327-4b82-85c5-cbe7eb48cf38"
# description_parsing(id)
#
# for product in products:
#     print(product.description)
#     print('---------------------')
#
# from doctor.functions.download import get_token, get_tk
# products = Product.objects.filter(category='Завтраки')
# c = 0
# n = 0
# for product in products:
#     n += 1
#     tk = get_tk(product.product_id)
#     try:
#         if tk[0]["assemblyCharts"][0]["technologyDescription"] != '':
#             c += 1
#             product.cooking_method = tk[0]["assemblyCharts"][0]["technologyDescription"]
#             product.save()
#     except:
#         pass
#     print(f'{n} - {c}')
#
#
#
# count_prosucts_labeled = len(Product.objects.filter(category='Гарниры').filter(
#         Q(ovd='True') | Q(ovd_sugarless='True') | Q(ovd_vegan='True') | Q(shd='True') | Q(shd_sugarless=True) |
#         Q(bd='True') | Q(vbd='True') | Q(nbd='True') | Q(nkd='True') | Q(vkd='True') |
#         Q(iodine_free='True') | Q(not_suitable='True')))
#
# count_prosucts_labeled = (Product.objects.filter(category='Салаты').filter(
#         ~Q(ovd='True') & ~Q(ovd_sugarless='True') & ~Q(ovd_vegan='True') & ~Q(shd='True') & ~Q(shd_sugarless=True) &
#         ~Q(bd='True') & ~Q(vbd='True') & ~Q(nbd='True') & ~Q(nkd='True') & ~Q(vkd='True') &
#         ~Q(iodine_free='True') & ~Q(not_suitable='True')))
#
#
# # проверяет есть ли блюда линии раздачи
# from django.db.models import Q
# from datetime import date
# set_menu = MenuByDay.objects.filter(date__gte=date.today())
# MenuByDay.objects.filter(date__gte=date.today())\
#                  .filter(Q(main__contains='cafe') | Q(salad__contains='cafe') |
#                         Q(garnish__contains='cafe') | Q(porridge__contains='cafe'))

#
# Бахмутов Дмитрий Александрович, breakfast, True 2023-04-12
# cafe-salad-889
# category = {
#     "продукты": 1,
#     "одежда": 2,
#     "услуги": 3
# }


""" конфиг nginx
server {
        server_name www.dev-sk.petrushkagroup.ru dev-sk.petrushkagroup.ru;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
                root /home/shumilin/hadassah;
        }
        location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
}
}

server {
    if ($host ~* ^www\.(.*)$) {
        return 301 https://dev-sk.petrushkagroup.ru$request_uri;
    }
}




"""