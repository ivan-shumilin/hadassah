import os
from datetime import date, time, datetime
from typing import Dict

import xlsxwriter
from xlsxwriter.worksheet import Worksheet

from nutritionist.constants import *
from nutritionist.models import Report


def sort_by_date(filtered_report):
    report = {}
    for index, item in enumerate(filtered_report):
        report.setdefault(str(item.date_create), []).append(item)
    return report


def sort_by_meal(report):
    report_ = {}
    for key, value in report.items():
        report_[key] = {}
        for index, item in enumerate(value):
            report_[key].setdefault(str(item.meal), []).append(item)
    return report_


def change_str_in_date(date_str):
    date_list = date_str.split('-')
    return date(int(date_list[0]), int(date_list[1]), int(date_list[2]))


def create_external_report(filtered_report: Report) -> Dict:
    """ Отчет для Hadassah. Создает словарь с отчетом по дням и диетам, в котором содержаться цена, сухпаек и кол-во """
    report = sort_by_date(filtered_report)
    report_ = sort_by_meal(report)

    money_total = 0
    count_total = 0
    money_zero_diet_total = 0
    count_zero_diet_total = 0
    money_emergency_food_total = 0
    count_emergency_food_total = 0

    for date_key, one_day_report in report_.items():
        report[date_key] = {}
        count_all = 0 # все рационы кроме "Нулевой диеты"
        count_emergency_food_all = 0
        count_just_wather = 0
        count_bd_2 = 0

        if change_str_in_date(date_key) >= date(2023, 5, 1):
            price_bouillon = 0
        else:
            price_bouillon = 90

        for meal_key in ['breakfast', 'lunch', 'afternoon', 'dinner']:
            meal_report = one_day_report.get(meal_key, [])
            # создать функцию, которая добаляет уникальные диеты в report
            report[date_key][meal_key] = {}
            users = list(set([item_report.user_id for item_report in meal_report]))

            for user in users:
                report_user_set = [report for report in meal_report if report.user_id == user]
                # if len([report_item for report_item in report_user_set if report_item.product_id=='426']) > 0 and \
                #         report_user_set[0].meal == 'dinner' and report_user_set[0].type_of_diet == 'БД день 2' or \
                #         len([report_item for report_item in report_user_set if report_item.product_id == '426']) == 0:
                if len([report_item for report_item in report_user_set if report_item.product_id in ['569', '568', '570']]) == 0:
                    for report_user in report_user_set:
                        report[date_key][meal_key].setdefault(str(report_user.type_of_diet), []).append(report_user)
                else:
                    for report_user in report_user_set:
                        report[date_key][meal_key].setdefault(f'{report_user.type_of_diet} + экстренное питание', []).append(report_user)

            for diet_key, on_diet_report in report[date_key][meal_key].items():
                count_items = len(set([user.user_id for user in (report[date_key][meal_key][diet_key])]))
                count_bouillon = \
                    len(set([user.user_id for user in (report[date_key][meal_key][diet_key])
                                if user.product_id == '426' and\
                                not (meal_key == 'dinner' and diet_key == 'БД день 2')]))
                count_emergency_food = \
                    len(set([user.user_id for user in (report[date_key][meal_key][diet_key])
                                if user.product_id in ['569', '568', '570']]))

                if "нулевая диета + экстренное питание" in diet_key.lower():
                    price = PRICE_ALL
                elif "нулевая диета" in diet_key.lower():
                    price = PRICE_JUST_WATHER
                    count_just_wather += count_items
                elif diet_key == 'БД день 2' and meal_key == 'afternoon':
                    price = PRICE_COUNT_BD_2
                    count_bd_2 += count_items
                else:
                    price = PRICE_ALL

                count_all += count_items
                count_emergency_food_all += count_emergency_food

                report[date_key][meal_key][diet_key] =\
                    {'count': count_items,
                     'count_bouillon': count_bouillon,
                     'count_emergency_food': count_emergency_food,
                     'money': (count_items * price) + (count_bouillon * price_bouillon) + (count_emergency_food * PRICE_EMERGENCY_FOOD)}

                # считает отдельно цену и количество нулевых диет
                if "нулевая диета" in diet_key.lower():
                    money_zero_diet_total += (count_items * price) + (count_bouillon * price_bouillon) + (
                            count_emergency_food * PRICE_EMERGENCY_FOOD)
                    count_zero_diet_total += count_items

        money = (count_all - count_just_wather - count_bd_2) * PRICE_ALL + \
                (count_just_wather * PRICE_JUST_WATHER) + \
                (count_bd_2 * PRICE_COUNT_BD_2) + \
                (count_bouillon * price_bouillon) + \
                (count_emergency_food_all * PRICE_EMERGENCY_FOOD)
        report[date_key]['Всего'] = {'count': count_all,
                                     'money': money}
        money_total += money
        count_total += count_all
        count_emergency_food_total += count_emergency_food_all
        money_emergency_food_total += count_emergency_food_all * PRICE_EMERGENCY_FOOD

    report['Итого'] = {'Всего за период': {'count': count_total, 'money': money_total}}
    report['Нулевая диета'] = {'count': count_zero_diet_total, 'money': money_zero_diet_total}
    report['Сухпаек'] = {'count': count_emergency_food_total, 'money': money_emergency_food_total}

    return report

def add_font_style(ws: Worksheet, style: str, text: str, row: int, *columns) -> None:
    """ Печатает одинаковый текст с одинаковым стилем на выбранные столбцы определенной строчкoй """
    for column in columns:
        ws.write(row, column, text, style)

def get_report(report: Dict, report_detailing: Dict,  date_start: datetime, date_finish: datetime) -> None:
    """ Создаёт excel файл с отчетом по блюдам """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Формируем путь к файлу внутри папки nutritionist/static
    file_path = os.path.join(current_dir, '../static/report.xlsx')
    wb = xlsxwriter.Workbook(file_path)

    def field_fill_white(ws: Worksheet, row_start: int, row_end: int, col_start: int, col_end: int) -> None:
        """ Заливает все поле на указанный квадрат листа белым """
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                ws.write(row, col, "", wb.add_format({"bg_color": "white"}))

    def number_to_digit(count_: int, money_: int) -> (str, str):
        """ Разделяет число на разряды - разделитель пробел """
        count_to_digit = '{0:,}'.format(count_).replace(',', ' ')
        money_to_digit = '{0:,}'.format(money_).replace(',', ' ')
        return count_to_digit, money_to_digit

    ws = wb.add_worksheet("Отчет")
    ws.set_default_row(20)

    font_first_title = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 18,
            "bold": False,
            "italic": False,
            "color": "383636",
            "align": "left",
            "fg_color": "white",
        }
    )

    font_table_cell = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "bold": False,
            "italic": False,
            "color": "383636",
            "align": "left",
            "fg_color": "white",
        }
    )

    font_total_format_header = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "bold": True,
            "align": "left",
            "fg_color": "white",
        }
    )

    font_number_room = wb.add_format({"font_name": "Arial", "font_size": 12, "align": "center", "fg_color": "white", })

    font_title_format = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 13,
            "bold": True,
            "italic": False,
            "fg_color": "203864",
            "align": "left",
            "valign": "vcenter",
            "color": "white",
        }
    )

    font_14_bold = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 14,
            "bold": True,
            "italic": False,
            "color": "000000",
            "fg_color": "white",
        }
    )

    font_dotted_border = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "fg_color": "white",
            "align": "left",
            "bold": False,
            "top": 4,
            "top_color": "203864",
        }
    )

    font_total_format = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "fg_color": "white",
            "bold": True,
            "align": "left",
            "top": 4,
            "top_color": "203864",
            "bottom": 1,
            "bottom_color": "000000",
        }
    )

    font_group_diet = wb.add_format({
        "font_name": "Arial",
        "font_size": 12,
        "fg_color": "white",
        "italic": True,
        "align": "left",
    })

    font_end_of_table = wb.add_format({
        "font_name": "Arial",
        "font_size": 12,
        "fg_color": "white",
        "italic": True,
    })

    # -------------------------------------------------------------------
    #                       страница "Отчёт"
    # -------------------------------------------------------------------

    field_fill_white(ws, 0, 300, 0, 50)

    ws.merge_range("A1:E1", "Отчет по лечебному питанию", font_first_title)
    ws.merge_range("A2:E2", "Круглосуточный стационар, Hadassah Medical Moscow", font_14_bold)
    ws.merge_range("A3:E3",
                   f'{date_start.day}.{date_start.month}.{date_start.year} - {date_finish.day}.{date_finish.month}.{date_finish.year}',
                   font_14_bold)

    row = 4

    count, money = number_to_digit(report["Итого"]["Всего за период"]["count"],
                                   report["Итого"]["Всего за период"]["money"])
    ws.write(row, 1, "Всего за период" + " (без учета экстренного питания)", font_total_format_header)
    ws.write(row, 3, count, font_total_format_header)
    ws.write(row, 4, f'{money}.00', font_total_format_header)

    row += 1
    count, money = number_to_digit(report["Нулевая диета"]["count"], report["Нулевая диета"]["money"])
    ws.write(row, 1, "      Нулевая диета", font_group_diet)
    ws.write(row, 3, f'{count}', font_group_diet)
    ws.write(row, 4, f'{money}.00', font_group_diet)
    add_font_style(ws, font_group_diet, "", row, 0, 2)

    row += 1
    count, money = number_to_digit(report["Итого"]["Всего за период"]["count"] - report["Нулевая диета"]["count"],
                                   report["Итого"]["Всего за период"]["money"] - report["Нулевая диета"]["money"])
    ws.write(row, 1, "      Остальные диеты", font_group_diet)
    ws.write(row, 3, f'{count}', font_group_diet)
    ws.write(row, 4, f'{money}.00', font_group_diet)
    add_font_style(ws, font_group_diet, "", row, 0, 2)

    row += 1
    count, money = number_to_digit(report["Сухпаек"]["count"], report["Сухпаек"]["money"])
    ws.write(row, 1, "+ Сухпаек (экстренное питание в нерабочие часы)", font_end_of_table)
    ws.write(row, 3, f'{count}', font_end_of_table)
    ws.write(row, 4, f'{money}.00', font_end_of_table)
    add_font_style(ws, font_end_of_table, "", row, 0, 2)

    row += 1
    count, money = number_to_digit(report["Итого"]["Всего за период"]["count"] + report["Сухпаек"]["count"],
                                   report["Итого"]["Всего за период"]["money"] + report["Сухпаек"]["money"])
    ws.write(row, 1, "Всего за период", font_total_format_header)
    ws.write(row, 3, count, font_total_format_header)
    ws.write(row, 4, f'{money}.00', font_total_format_header)

    row += 2
    headers = ["Учетный день", "Прием пищи", "Рацион", "Количество", "Сумма, руб."]
    for col, header in enumerate(headers):
        ws.write(row, col, header, font_title_format)

    ws.set_row(row, 35)

    row += 1
    for date, meal_info in report.items():
        if date.lower() != "нулевая диета" and date.lower() != "сухпаек":
            if date.lower() != "итого":
                ws.write(row, 0, date, font_table_cell)
            for meal, type_of_diet in meal_info.items():
                first_row = row
                if meal == "Всего":
                    add_font_style(ws, font_total_format, "", row, 0, 2)
                    count, money = number_to_digit(type_of_diet["count"], type_of_diet["money"])
                    ws.write(row, 1, meal + ' ' + '(без учета экстренного питания)', font_total_format)
                    ws.write(row, 3, count, font_total_format)
                    ws.write(row, 4, f'{money}.00', font_total_format)
                elif meal != "Всего за период":
                    if meal == "breakfast":
                        ws.write(row, 1, "Завтрак", font_table_cell)
                    else:
                        ws.write(row, 0, "", font_dotted_border)
                        ws.write(
                            row,
                            1,
                            {"lunch": "Обед", "afternoon": "Полдник", "dinner": "Ужин"}.get(meal, meal),
                            font_dotted_border,
                        )

                    for diet, diet_info in type_of_diet.items():
                        style = font_table_cell
                        if row == first_row:
                            if meal != "breakfast":
                                style = font_dotted_border
                        # убирает границы для столбцов A B, если там не надо писать прием пищи
                        else:
                            add_font_style(ws, style, "", row, 0, 1)

                        count, money = number_to_digit(diet_info["count"], diet_info["money"])
                        ws.write(row, 2, diet, style)
                        ws.write(row, 3, count, style)
                        ws.write(row, 4, f'{money}.00', style)
                        row += 1
        row += 1

    ws.set_column("A:E", 20)  # 4.87 cm
    ws.set_column("B:B", 30)
    ws.set_column("C:C", 30)
    ws.set_column("D:D", 19)
    ws.set_column("E:E", 19)

    field_fill_white(ws, 0, row + 1, 5, 50)
    field_fill_white(ws, row + 1, row + 1 + 5, 0, 50)

    # -------------------------------------------------------------------
    #                       страница "Детальный"
    # -------------------------------------------------------------------

    ws_detail = wb.add_worksheet("Детальный")
    ws_detail.set_default_row(20)

    ws_detail.merge_range("A1:E1", "Детализация к отчету по лечебному питанию", font_first_title)
    ws_detail.merge_range("A2:E2", "Круглосуточный стационар, Hadassah Medical Moscow", font_14_bold)
    ws_detail.merge_range("A3:E3", f'{date_start.day}.{date_start.month}.{date_start.year}'
                                   f' - {date_finish.day}.{date_finish.month}.{date_finish.year}', font_14_bold)

    headers = ["Учетный день", "Прием пищи", "Рацион", "ФИО", "№ палаты"]
    for col, header in enumerate(headers):
        ws_detail.write(4, col, header, font_title_format)

    field_fill_white(ws_detail, 3, 3, 0, 5)

    row = 5
    for date, date_info in report_detailing.items():
        for meal, meal_info in date_info.items():
            for diet, diet_info in meal_info.items():
                for patient, patient_info in diet_info.items():
                    ws_detail.write(row, 0, date, font_table_cell)
                    if meal == 'breakfast':
                        ws_detail.write(row, 1, 'Завтрак', font_table_cell)
                    elif meal == 'lunch':
                        ws_detail.write(row, 1, 'Обед', font_table_cell)
                    elif meal == 'afternoon':
                        ws_detail.write(row, 1, 'Полдник', font_table_cell)
                    elif meal == 'dinner':
                        ws_detail.write(row, 1, 'Ужин', font_table_cell)
                    ws_detail.write(row, 2, diet, font_table_cell)
                    ws_detail.write(row, 3, patient, font_table_cell)
                    ws_detail.write(row, 4, patient_info[0] if patient_info[0] != "Не выбрано" else "——", font_number_room)
                    row += 1

    ws_detail.set_row(4, 35)
    ws_detail.set_column("A:E", 19)  # 4.87 cm

    field_fill_white(ws_detail, 0, row + 5, 5, 50)
    field_fill_white(ws_detail, row, row + 5, 0, 50)

    wb.close()
    return


def create_external_report_detailing(filtered_report: Report) -> Dict:
    """ Создает детальный отчет """
    report = {}
    report_ = {}
    for index, item in enumerate(filtered_report):
        report.setdefault(str(item.date_create), []).append(item)

    for key, value in report.items():
        report_[key] = {}
        for index, item in enumerate(value):
            report_[key].setdefault(str(item.meal), []).append(item)

    for key1, value1 in report_.items():
        report[key1] = {}

        for key2, value2 in value1.items():
            report[key1][key2] = {}
            for index, item in enumerate(value2):
                if item.type == 'emergency-night':
                    item.type_of_diet = 'Сухпаек'
                elif item.type == 'emergency-day':
                    item.type_of_diet += ' + экстренное питание'
                report[key1][key2].setdefault(str(item.type_of_diet), []).append(item)
            for key3, value3 in report[key1][key2].items():
                test = {}
                for item in report[key1][key2][key3]:
                    test[item.user_id.full_name] = (item.user_id.room_number, item.user_id.floor, item.user_id.department, item.type)
                report[key1][key2][key3] = test
    return report


def get_brakery_magazine(meal: str, today: datetime, menu: set) -> None:
    """ Создает бракеражный журнал по приемам пищи """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../static/brakery.xlsx')
    wb = xlsxwriter.Workbook(file_path)

    ws = wb.add_worksheet("Бракераж")
    font_first_title = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "bold": True,
            "align": "center",
        }
    )

    font_title_centered_with_border = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "center",
            'border': 1,
            "valign": "vcenter",
            'text_wrap': True
        }
    )

    font_align_left_top = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "left",
            'border': 1,
            "valign": "top",
            'text_wrap': True
        }
    )

    font_align_center_top = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "center",
            'border': 1,
            "valign": "top",
        }
    )

    font_for_comments = wb.add_format(
        {
            "font_name": "Arial",
            "italic": True,
            "font_size": 8,
            "align": "center",
            'border': 1,
            "valign": "top",
        }
    )

    font_cell_centered_without_border = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "center",
        }
    )

    font_right_without_border = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "right",
        }
    )

    font_for_meal = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "left",
            'bold': True
        }
    )

    months_ru = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }

    if today > datetime.today():
        today = datetime.today()

    # Форматирование даты
    # Форматирование даты
    formatted_date = "{0} {1} {2} г.".format(today.day, months_ru[today.month], today.year)

    today_full_info = today.strftime("%d.%m.%Y %H:%M")
    today_time = today.strftime("%H:%M")

    ws.merge_range('H1:I1', 'СанПиН 2.3/2.4.3590-20 ', font_right_without_border)
    ws.merge_range('A2:B2', 'ООО "Петрушка Ск"', font_cell_centered_without_border)

    ws.merge_range('A3:B3', formatted_date, font_cell_centered_without_border)
    ws.merge_range("A4:I4", "Журнал бракеража готовой кулинарной продукции", font_first_title)

    cell_merge_for_title = ['A', 'B', 'C', 'D', 'E', 'H', 'I']
    titles = ['Дата и час изготовления блюда', ' Время снятия бракеража', 'Наименование блюда, кулинарного изделия',
              'Результаты органолептической оценки и степени готовности блюда, кулинарного изделия',
              'Разрешение к реализации блюда, кулинарного изделия',
              'Результаты взвешивания порционных блюд', 'Примечание*']

    ws.merge_range('F6:G9', 'Подписи членов бракеражной комиссии', font_title_centered_with_border)

    col = 0
    number = 1
    for cell_letter in range(len(titles)):
        letter = cell_merge_for_title[cell_letter]
        ws.merge_range(letter + '6' + ':' + letter + '9', titles[cell_letter], font_title_centered_with_border)
        ws.write(9, col, number, font_title_centered_with_border)
        col += 1 if letter != 'E' else 3
        number += 1 if letter != 'E' else 2
    ws.merge_range('F10:G10', 6, font_title_centered_with_border)

    ws.set_column("A:A", 15)  # 4.87 cm
    ws.set_column("B:B", 10)
    ws.set_column("C:C", 21)
    ws.set_column("D:D", 18)
    ws.set_column("E:E", 15)
    ws.set_column("F:G", 7)
    ws.set_column("H:H", 14)
    ws.set_column("I:I", 12)

    ws.merge_range('A11:I11', meal, font_for_meal)

    row = 11
    for product in menu:
        ws.write(row, 0, today_full_info, font_align_left_top)
        ws.write(row, 1, today_time, font_align_center_top)
        ws.write(row, 2, product, font_align_left_top)
        ws.write(row, 3, 'Отлично', font_for_comments)
        ws.write(row, 4, 'Разрешено', font_for_comments)
        ws.write(row, 7, 'Соответствует', font_for_comments)
        add_font_style(ws, font_for_comments, '', row, 5, 6, 8)
        row += 1

    wb.close()
    return
