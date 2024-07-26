import logging

from django.core.management.base import BaseCommand
import requests, calendar, datetime, os
from datetime import datetime, date
from django.core import management

logger = logging.getLogger('main_logger')


URL = 'https://cloud-api.yandex.net/v1/disk/resources'
TOKEN = 'y0_AQAEA7qkHGTtAADLWwAAAADLdv2Vzl_VDfyET4ekZCPJK_nQZ3UUrqY'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}


# def create_backup():
#     name = str(date.today()) + '.json'
#     with open(name, 'w', encoding='utf-8') as outfile:
#         management.call_command('dumpdata',
#                                 'nutritionist.product',
#                                 'nutritionist.timetable',
#                                 'nutritionist.productlp',
#                                 'nutritionist.timetablelp',
#                                 stdout=outfile)


def create_backup():
    filename = str(date.today()) + '_' + str(datetime.now().hour) + '.json'
    with open(filename, 'w', encoding='utf-8') as outfile:
        management.call_command('dumpdata',
                                'nutritionist.product',
                                'nutritionist.timetable',
                                'nutritionist.productlp',
                                'nutritionist.timetablelp',
                                'nutritionist.customuser',
                                'nutritionist.userstoday',
                                'nutritionist.menubyday',
                                'nutritionist.usersreadyorder',
                                'nutritionist.menubydayreadyorder',
                                'nutritionist.commentproduct',
                                'nutritionist.report',
                                'nutritionist.productstorage',
                                'nutritionist.ingredient',
                                'nutritionist.ttk',
                                'auth.group',
                                stdout=outfile)


def create_folder(path):
    # URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    # TOKEN = 'AQAAAAAnzmiwAAgF_TNw9en0lUKImDw8u7S2eQk'
    # headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

    """Создание папки. \n path: Путь к создаваемой папке."""
    try:
        requests.put(f'{URL}?path={path}', headers=headers)
    except:
        pass


def upload_file(loadfile, savefile, replace=True):
    # URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    # TOKEN = 'AQAAAAAnzmiwAAgF_TNw9en0lUKImDw8u7S2eQk'
    # headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
    """Загрузка файла.
    loadfile: Путь к загружаемому файлу
    savefile: Путь к файлу на Диске
    replace: true or false Замена файла на Диске"""

    res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    logger.info(f'Upload file: {loadfile}')
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file': f})
        except KeyError:
            print(res)
            return res


class Command(BaseCommand):  # https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
    help = 'Dump database in yandex disk'

    def handle(self, *args, **options):
        filename = str(date.today()) + '_' + str(datetime.now().hour) + '.json'
        logger.info(f'Create backup. Time: {datetime.now()}')
        create_backup()
        logger.info(f'Create folder {"backup" + "/" + str(date.today())}')
        create_folder('backup' + '/' + str(date.today()))
        answer = upload_file(filename, 'backup' + '/' + str(date.today()) + '/' + filename)
        return answer
