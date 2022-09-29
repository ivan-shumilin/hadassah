from django.core.management.base import BaseCommand
import sys
import time
import telepot
from telepot.loop import MessageLoop
from nutritionist.models import BotChatId


class Command(BaseCommand):
    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
        bot = telepot.Bot(TOKEN)
        if content_type == 'text':
            bot.sendMessage(chat_id, msg['text'])
            base_chat_id = BotChatId()
            if len(BotChatId.objects.filter(chat_id=chat_id)) == 0:
                base_chat_id.chat_id = chat_id
                base_chat_id.save()


    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)
