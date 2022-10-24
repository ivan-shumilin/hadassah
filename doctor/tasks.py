from celery import shared_task
import telepot
from nutritionist.models import BotChatId

@shared_task()
def send_messang():
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    attention = u'\u2757\ufe0f'
    bot = telepot.Bot(TOKEN)
    # все номера chat_id
    messang = f'test'
    for item in BotChatId.objects.all():
        bot.sendMessage(item.chat_id, messang, parse_mode="html")