"""
Для отчетов по Report
Восстановление истории изменеий пациента
# """
# from nutritionist.models import Report, CustomUser, ProductLp, Product, MenuByDay
#
# ProductLp.objects.filter(Q(timetablelp__type_of_diet=translated_diet))
#
# from scripts.copy_diets import copy_diet
# copy_diet()
#
# # получаем блюда
# for meal in result.values():
#     for cat in meal.values():
#         if cat != {}:
#             cat = dict(sorted(cat.items()))
#
# from nutritionist.models import ModifiedDish, CustomUser
#
# user = CustomUser.objects.get(full_name="Млынская Олеся Григорьевна")
# reports = ModifiedDish.objects.filter(date='2023-11-01', meal="breakfast")
# for i, rr in enumerate(reports):
#     for r in rr.product_id.split(','):
#         if 'cafe' in r:
#             id = r.split('-')[2]
#             name = Product.objects.get(id=id).name + '(ЛП)'
#         else:
#             name = ProductLp.objects.get(id=r).name + '(раздача)'
#         print(f'{i + 1}. {rr.user_id.full_name} - {name} - {rr.meal} - {rr.status}')
#
# menu = MenuByDay.objects.filter(date='2023-11-01', meal="breakfast")
# for i, rr in enumerate(menu):
#     for r in rr.product_id.split(','):
#         if 'cafe' in r:
#             id = r.split('-')[2]
#             name = Product.objects.get(id=id).name + '(ЛП)'
#         else:
#             name = ProductLp.objects.get(id=r).name + '(раздача)'
#         print(f'{i + 1}. {rr.user_id.full_name} - {name} - {rr.meal}')