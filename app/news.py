from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import telegram
import random
from app.utils import *


def news_handler(bot, update, msg_list):
    if msg_list[1] in ["news","News"]:
        news_creds = open("api/news", "r")
        creds = news_creds.read()
        url = ('https://newsapi.org/v2/top-headlines?'
               'country=in&'
               'apiKey='+creds)
        result = requests.get(url).json()['articles']
        data = ''
        count = 0
        for item in result:
            count += 1
            if count == 6:
                break
            data += item['title']+"\n\n"  # +item['description']+"\n\n"
        update.message.reply_text(data)
