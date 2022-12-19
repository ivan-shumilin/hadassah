# def test(request):
#     """Создаем json со всеми продуктами лечебного питания."""
#     from openpyxl import load_workbook
#     name_files = [['I_des.xlsx','TTK_des.xlsx', 'десерт'],
#                   ['I_dr.xlsx', 'TTK_dr.xlsx', 'напиток'],
#                   ['I_fr.xlsx', 'TTK_fr.xlsx', 'фрукты'],
#                   ['I_gr.xlsx', 'TTK_gr.xlsx', 'гарнир'],
#                   ['I_main.xlsx', 'TTK_main.xlsx', 'основной'],
#                   ['I_om.xlsx', 'TTK_om.xlsx', 'основной'],
#                   ['I_pr.xlsx', 'TTK_pr.xlsx', 'каша'],
#                   ['I_sd.xlsx', 'TTK_sd.xlsx', 'салат'],
#                   ['I_soup.xlsx', 'TTK_soup.xlsx', 'суп'],
#                  ]
#     result = []
#     result1 = []
#     for name_file in name_files:
#         wb = load_workbook(f'ttk/{name_file[0]}')
#         wb1 = load_workbook(f'ttk/{name_file[1]}')
#         category = name_file[2]
#         sheet_names = wb.get_sheet_names()
#         sheet_names1 = wb1.get_sheet_names()
#         product1 = {}
#
#         for sheet_name in sheet_names1:
#             sheet1 = wb1.get_sheet_by_name(sheet_name)
#             info_tk = sheet1['A8'].value
#             try:
#                 product1['number_tk'] = info_tk.split(' ')[3]
#             except:
#                 print('Ошибка - ', sheet1['A8'].value, sheet1['A7'].value, sheet1['A9'].value)
#             did_you_find_the_weight = False
#             for cell in range(1, 300):
#                 if did_you_find_the_weight == False:
#                     try:
#                         w = str(sheet1[f'Z{str(cell)}'].value)
#                         product1['weight'] = float(w.replace(',', '.'))
#                         did_you_find_the_weight = True
#                     except:
#                         pass
#
#                 if 'Белки' in str(sheet1[f'A{str(cell)}'].value):
#                     product1['fiber'] = sheet1[f'A{str(cell + 1)}'].value
#                     product1['carbohydrate'] = sheet1[f'I{str(cell + 1)}'].value
#                     product1['fat'] = sheet1[f'D{str(cell + 1)}'].value
#                     product1['energy'] = sheet1[f'N{str(cell + 1)}'].value
#                     break
#             result1.append(product1)
#             product1 = {}
#
#
#         product = {}
#
#         def spider(res, level, line, sheet):
#             flag_count = False
#             res_start = res
#             res = []
#             level += 1
#             # delta = 0
#             while True:
#                 # delta += 1
#
#                 line += 1
#                 name = (sheet[f'D{str(line)}'].value).strip() if sheet[f'D{str(line)}'].value != None else ''
#                 # если конец списка
#                 if name == '':
#                     if len(res) == 0:
#                         return res_start, line + 1, 'finish'
#                     else:
#                         res.append(name)
#                         return f'{res_start}({", ".join(res)})', line, 'finish'
#                 # если конец подсписка
#                 if sheet[f'C{str(line + 1)}'].value != None:
#                     if int(sheet[f'C{str(line + 1)}'].value) < level:
#                         if len(res) == 0:
#                             return name, line, 'next'
#                         elif flag_count == True and len(res) == 1:
#                             return ", ".join(res), line - 1, 'next'
#                         else:
#                             res.append(name)
#                             return f'{res_start}({", ".join(res)})', line, 'next'
#                 else:
#                     if len(res) == 0:
#                         return name, line, 'next'
#                     else:
#                         res.append(name)
#                         return f'{res_start}({", ".join(res)})', line, 'next'
#                 # если подсписок продолжается
#                 if sheet[f'C{str(line + 1)}'].value == str(level):
#                     res.append(name)
#                 # если есть подсписок
#                 if sheet[f'C{str(line + 1)}'].value == str(level + 1):
#                     name, line, status = spider(name, level, line, sheet)
#                     if len(name.split(' ')) == 1:
#                         flag_count = True
#
#                     res.append(name)
#
#
#         for sheet_name in sheet_names:
#             sheet = wb.get_sheet_by_name(sheet_name)
#
#                 # if sheet1[f'D{str(cell)}'].value == 'Жиры':
#                 #     print(sheet1[f'D{str(cell)}'].value, sheet1[f'D{str(cell + 1)}'].value)
#                 # if sheet1[f'I{str(cell)}'].value == 'Углеводы':
#                 #     print(sheet1[f'I{str(cell)}'].value, sheet1[f'I{str(cell + 1)}'].value)
#                 # if sheet1[f'N{str(cell)}'].value == 'ккал':
#                 #     print(sheet1[f'N{str(cell)}'].value, sheet1[f'N{str(cell + 1)}'].value)
#
#
#
#             product['name'] = sheet['A1'].value
#             info_tk = sheet['A3'].value
#             product['number_tk'] = info_tk.split(' ')[3]
#             level = 1
#             name = ""
#             # result = ""
#             status = "next"
#             composition = ""
#             line = 5
#             while True:
#                 line += 1
#                 name = sheet[f'D{str(line)}'].value
#                 if name == None:
#                     break
#                 # если конец списка
#                 if sheet[f'C{str(line + 1)}'].value == None:
#                     composition += name.lower().strip() + ', '
#                     break
#                 # если нет подсписка
#                 if sheet[f'C{str(line + 1)}'].value == str(level):
#                     composition += name.lower().strip() + ', '
#                 else:
#                     name, line, status = spider(name, level, line, sheet)
#                     composition += name.lower().strip() + ', '
#                 if status == 'finish':
#                     break
#
#
#             composition = composition.replace(' п/ф', '').\
#                   replace('п/ф', '').\
#                   replace(' п/ф', '').\
#                   replace('с/м', ''). \
#                   replace(' с/м', ''). \
#                   replace('с/с', ''). \
#                   replace(' с/с', ''). \
#                   replace(' зам.', ''). \
#                   replace(' очищ.', ''). \
#                   replace(' пост', ''). \
#                   replace(' (', '('). \
#                   replace('(продукт полутвердый)', '').capitalize()[:-2]
#             print(composition)
#             product['composition'] = composition
#             product['category'] = category
#             result.append(product)
#             product = {}
#     """ Обьединим два результата """
#     for item1 in result1:
#         for item in result:
#             if 'number_tk' in item and 'number_tk' in item1:
#                 if item['number_tk'] == item1['number_tk']:
#                     item['fiber'] = item1['fiber'] if 'fiber' in item1 else None
#                     item['carbohydrate'] = item1['carbohydrate'] if 'carbohydrate' in item1 else None
#                     item['fat'] = item1['fat'] if 'fat' in item1 else None
#                     item['energy'] = item1['energy'] if 'energy' in item1 else None
#                     item['weight'] = item1['weight'] if 'weight' in item1 else None
#
#     return render(request, 'test.html', {})#