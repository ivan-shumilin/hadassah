import datetime
import os

from collections import defaultdict
from datetime import timedelta, time

import django
import xlsxwriter
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hadassah.settings')
django.setup()

from nutritionist.models import Report, CustomUser


def get_user_info(user_id, users) -> dict:
    for user in users:
        if user_id == user['id']:
            return user


def create_analysis_2023_12():
    wb = xlsxwriter.Workbook("static/report_2023.xlsx")
    ws = wb.add_worksheet("Отчет")

    font_14_bold = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 14,
            "bold": True,
            "italic": False,
            "color": "000000",
        }
    )

    font_title = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "bold": True,
            "italic": False,
            "color": "000000",
            'align': 'center'
        }
    )

    font_table_cell = wb.add_format(
        {
            "font_name": "Arial",
            "font_size": 12,
            "bold": False,
            "italic": False,
            "color": "383636",
            "align": "center",
        }
    )

    ws.merge_range("A1:E1", "Отчет по питанию за 2023-12-01 до 2023-12-31", font_14_bold)

    date_start = datetime.date(2023, 12, 1)
    date_finish = datetime.date(2023, 12, 31)

    # (1) Общее число рационов (приемов пищи) КС - done
    total_count_food = 0
    reports = Report.objects.filter(
        date_create__range=(date_start, date_finish)
    ).values('meal').annotate(total_meal_count=Count('user_id_id', distinct=True))

    for meal in reports:
        total_count_food += meal['total_meal_count'] # 928

    ws.merge_range("A4:B4", 'Общее число рационов', font_title)
    ws.write(3, 2, str(total_count_food), font_table_cell)

    # (2) Два ряда данных по дням: число пациентов КС и число пациентов КС с комментарием - done
    dct_for_patient = {}

    reports_for_patient = Report.objects.filter(
        date_create__range=(date_start, datetime.date(2024, 1, 1))
    ).values('meal', 'date_create', 'user_id_id')

    users = CustomUser.objects.values('id', 'receipt_time', 'receipt_date', 'comment').distinct('id')

    for day in range(1, 32):
        date = datetime.date(2023, 12, day)

        # dct = Report.objects.filter(date_create=date).values('meal').annotate(
        #     num_users=Count('user_id_id', distinct=True))

        dct_to_comments = Report.objects.filter(date_create=date).values('user_id_id').distinct('user_id_id')

        total_patient_count_by_day = 0

        # for meal in dct:
        #     total_patient_count_by_day += meal['num_users']

        dct_for_patient.setdefault(date, [0, 0])
        # dct_for_patient[date][0] += total_patient_count_by_day

        for patient in dct_to_comments:
            dct_for_patient[date][0] += 1
            user_info = get_user_info(patient['user_id_id'], users)
            if user_info['comment'] != '':
                dct_for_patient[date][1] += 1

            if (user_info['receipt_time'] >= time(19, 0, 0) and
                    (user_info['receipt_date'] == date - timedelta(days=1)) and
                    (date - timedelta(days=1) != datetime.date(2023, 11, 30))):

                dct_for_patient[date - timedelta(days=1)][0] += 1
                if user_info['comment'] != '':
                    dct_for_patient[date - timedelta(days=1)][1] += 1

    date = datetime.date(2024, 1, 1)
    dct_to_comments_to_31 = Report.objects.filter(date_create=date).values('user_id_id').distinct('user_id_id')

    for patient in dct_to_comments_to_31:
        user_info = get_user_info(patient['user_id_id'], users)

        if user_info['receipt_time'] >= time(19, 0, 0) and \
                (user_info['receipt_date'] == date - timedelta(days=1)):
            dct_for_patient[date - timedelta(days=1)][0] += 1
            if user_info['comment'] != '':
                dct_for_patient[date - timedelta(days=1)][1] += 1



    # for report in reports_for_patient:
    #
    #     if report['date_create'] != datetime.date(2024, 1, 1):
    #         dct_for_patient.setdefault(report['date_create'], [0, 0])  # total and with comments
    #         dct_for_patient[report['date_create']][0] += 1
    #
    #     user_info = get_user_info(report['user_id_id'], users)
    #
    #     if user_info['comment'] != '':
    #         dct_for_patient[report['date_create']][1] += 1
    #
    #     if report['date_create'] != datetime.date(2023, 12, 1):
    #         if user_info['receipt_time'] >= time(19, 0, 0) and \
    #                 (user_info['receipt_date'] == report['date_create'] - timedelta(days=1)):
    #             dct_for_patient[report['date_create'] - timedelta(days=1)][0] += 1
    #             if user_info['comment'] != '':
    #                 dct_for_patient[report['date_create']][1] += 1

    ws.merge_range("A7:C7", "Число пациентов", font_title)
    ws.write(7, 0, 'Дата', font_table_cell)
    ws.write(7, 1, 'Всего', font_table_cell)
    ws.write(7, 2, 'С комментариями', font_table_cell)

    for day in range(1, 32):
        ws.write(7 + day, 0, str(datetime.date(2023, 12, day)), font_table_cell)
        ws.write(7 + day, 1, dct_for_patient[datetime.date(2023, 12, day)][0], font_table_cell)
        ws.write(7 + day, 2, dct_for_patient[datetime.date(2023, 12, day)][1], font_table_cell)

    # (3) Кол-во добавленных позиций через tool корректировки по дням
    # или в целом за месяц (имеются в виду и дополнительные, и в рамках замен)

    # (4) Кол-во блюд с линии раздачи по дням или в целом за месяц - done

    total_product_2023_12 = Report.objects.filter(
        date_create__range=(date_start, date_finish),
        product_id__icontains='cafe'
    ).values('date_create', 'product_id')

    product_dict_by_date = defaultdict(int)
    for date in total_product_2023_12:
        product_dict_by_date[date['date_create']] += date['product_id'].count('cafe')

    ws.merge_range("E7:F7", "Кол-во блюд с линии раздачи", font_title)
    ws.write(7, 4, 'Дата', font_table_cell)
    ws.write(7, 5, 'Количество', font_table_cell)
    row = 1
    for date, count in product_dict_by_date.items():
        ws.write(7 + row, 4, str(date), font_table_cell)
        ws.write(7 + row, 5, count, font_table_cell)
        row += 1

    # (5) Кол-во случаев экстренного питания в целом за месяц без учета поступлений
    # в нерабочие часы (то есть экстренные поступления в рабочие часы + экстренная смена диеты)

    reports_for_emergency_count = Report.objects.filter(
        date_create__range=(date_start, date_finish),
        type='emergency-day'
    ).count()

    ws.merge_range("H7:J7", "Кол-во экстренного питания (в рабочие часы)", font_title)
    ws.write(6, 10, reports_for_emergency_count, font_table_cell)

    ws.set_column("A:J", 17)  # 4.87 cm
    wb.close()


if __name__ == '__main__':
    create_analysis_2023_12()
