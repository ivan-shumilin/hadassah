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
    """ Отчет для Hadassah. Создает словарь с отчетом по дням и диетам, в котором содержаться цена, сухпаек и кол-во"""
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
                if (diet_key in ['Нулевая диета', 'Нулевая диета (Э)', 'Нулевая диета (П)'] +
                        ['Нулевая диета + бульон', 'Нулевая диета (Э) + бульон', 'Нулевая диета (П) + бульон']):
                    price = price_just_wather
                    count_just_wather += count_items

                elif diet_key == 'БД день 2' and meal_key == 'afternoon':
                    price = price_count_bd_2
                    count_bd_2 += count_items
                else:
                    price = price_all

                count_all += count_items
                count_emergency_food_all += count_emergency_food

                report[date_key][meal_key][diet_key] =\
                    {'count': count_items,
                     'count_bouillon': count_bouillon,
                     'count_emergency_food': count_emergency_food,
                     'money': (count_items * price) + (count_bouillon * price_bouillon) + (count_emergency_food * price_emergency_food)}

                # считает отдельно цену и количество нулевых диет
                if "Нулевая диета" in diet_key:
                    money_zero_diet_total += (count_items * price) + (count_bouillon * price_bouillon) + (
                            count_emergency_food * price_emergency_food)
                    count_zero_diet_total += count_items

        money = (count_all - count_just_wather - count_bd_2) * price_all + \
                (count_just_wather * price_just_wather) + \
                (count_bd_2 * price_count_bd_2) + \
                (count_bouillon * price_bouillon) + \
                (count_emergency_food_all * price_emergency_food)
        report[date_key]['Всего'] = {'count': count_all,
                                     'money': money}
        money_total += money
        count_total += count_all
        count_emergency_food_total += count_emergency_food_all
        money_emergency_food_total += count_emergency_food_all * price_emergency_food

    report['Итого'] = {'Всего за период': {'count': count_total, 'money': money_total}}
    report['Нулевая диета'] = {'count': count_zero_diet_total, 'money': money_zero_diet_total}
    report['Сухпаек'] = {'count': count_emergency_food_total, 'money': money_emergency_food_total}

    return report


def get_report(report: Dict, report_detailing: Dict,  date_start: datetime, date_finish: datetime) -> None:
    """Создаёт excel файл с отчетом по блюдам"""

    wb = xlsxwriter.Workbook("static/report.xlsx")

    def add_font_style(style: str, text: str, row: int, *columns) -> None:
        """ Печатает одинаковый текст с одинаковым стилем на выбранные столбцы определенной строчкoй """
        for column in columns:
            ws.write(row, column, text, style)

    def field_fill_white(ws: Worksheet, row_start: int, row_end: int, col_start: int, col_end: int) -> None:
        """ Заливает все поле на указанный квадрат листа белым"""
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                ws.write(row, col, "", wb.add_format({"bg_color": "white"}))

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

    font_number_room = wb.add_format({"font_name": "Arial", "font_size": 12, "align": "center", "fg_color": "white",})

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

    font_16_bold = wb.add_format(
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
            "fg_color": "white",
            "align": "left",
            "bold": False,
            "top": 4,
            "top_color": "203864",
        }
    )

    font_total_format = wb.add_format(
        {
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
        "fg_color": "white",
        "italic": False,
        "align": "left",
    })

    # -------------------------------------------------------------------
    #                       страница "Отчёт"
    # -------------------------------------------------------------------

    field_fill_white(ws, 0, 300, 0, 50)

    ws.merge_range("A1:E1", "Отчет по лечебному питанию", font_first_title)
    ws.merge_range("A2:E2", "Круглосуточный стационар, Hadassah Medical Moscow", font_16_bold)
    ws.merge_range("A3:E3", f'{date_start.day}.{date_start.month}.{date_start.year} - {date_finish.day}.{date_finish.month}.{date_finish.year}',
                   font_16_bold)

    headers = ["Учетный день", "Прием пищи", "Рацион", "Количество", "Сумма, руб."]
    for col, header in enumerate(headers):
        ws.write(4, col, header, font_title_format)

    row = 5
    for date, meal_info in report.items():
        if date != "Нулевая диета" and date != "Сухпаек":
            if date != "Итого":
                ws.write(row, 0, date, font_table_cell)
            for meal, type_of_diet in meal_info.items():
                first_row = row
                if meal in ["Всего", "Всего за период"]:
                    add_font_style(font_total_format, "", row, 0, 2)
                    ws.write(row, 1, meal, font_total_format)
                    ws.write(row, 3, type_of_diet["count"], font_total_format)
                    ws.write(row, 4, f'{type_of_diet["money"]}.00', font_total_format)
                else:
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
                            add_font_style(style, "", row, 0, 1)
                        ws.write(row, 2, diet, style)
                        ws.write(row, 3, diet_info["count"], style)
                        ws.write(row, 4, f'{diet_info["money"]}.00', style)
                        row += 1
        row += 1

    ws.write(row - 2, 1, "—Нулевая диета", font_group_diet)
    ws.write(row - 2, 3, f'{report["Нулевая диета"]["count"]}', font_group_diet)
    ws.write(row - 2, 4, f'{report["Нулевая диета"]["money"]}.00', font_group_diet)
    add_font_style(font_group_diet, "", row - 2, 0, 2)

    ws.write(row - 1, 1, "—Остальные диеты ", font_group_diet)
    ws.write(row - 1, 3, f'{ report["Итого"]["Всего за период"]["count"] - report["Нулевая диета"]["count"]}', font_group_diet)
    ws.write(row - 1, 4, f'{report["Итого"]["Всего за период"]["money"] - report["Нулевая диета"]["money"]}.00', font_group_diet)
    add_font_style(font_group_diet, "", row - 1, 0, 2)

    ws.write(row, 1, "Сухпаек", font_total_format)
    ws.write(row, 3, f'{report["Сухпаек"]["count"]}', font_total_format)
    ws.write(row, 4, f'{report["Сухпаек"]["money"]}.00', font_total_format)
    add_font_style(font_total_format, "", row, 0, 2)

    ws.set_row(4, 35)
    ws.set_column("A:E", 19)  # 4.87 cm

    field_fill_white(ws, 0, row + 1, 5, 50)
    field_fill_white(ws, row + 1, row + 1 + 5, 0, 50)

    # -------------------------------------------------------------------
    #                       страница "Детальный"
    # -------------------------------------------------------------------

    ws_detail = wb.add_worksheet("Детальный")
    ws_detail.set_default_row(20)

    ws_detail.merge_range("A1:E1", "Детализация к отчету по лечебному питанию", font_first_title)
    ws_detail.merge_range("A2:E2", "Круглосуточный стационар, Hadassah Medical Moscow", font_16_bold)
    ws_detail.merge_range("A3:E3", f'{date_start.day}.{date_start.month}.{date_start.year}'
                                   f' - {date_finish.day}.{date_finish.month}.{date_finish.year}', font_16_bold)

    headers = ["Учетный день", "Прием пищи", "Рацион", "ФИО", "№ палаты"]
    for col, header in enumerate(headers):
        ws_detail.write(4, col, header, font_title_format)

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
                    ws_detail.write(row, 4, patient_info if patient_info != "Не выбрано" else "——", font_number_room)
                    row += 1

    ws_detail.set_row(4, 35)
    ws_detail.set_column("A:E", 19)  # 4.87 cm

    field_fill_white(ws_detail, 0, row + 5, 5, 50)
    field_fill_white(ws_detail, row, row + 5, 0, 50)

    wb.close()
    return


def create_external_report_detailing(filtered_report):
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
                report[key1][key2].setdefault(str(item.type_of_diet), []).append(item)
            for key3, value3 in report[key1][key2].items():
                test = {}
                for item in report[key1][key2][key3]:
                    test[item.user_id.full_name] = item.user_id.room_number
                report[key1][key2][key3] = test
    return report
