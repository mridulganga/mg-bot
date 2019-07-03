from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

def get_image_url(animal):
    if animal in ["dog","bark","bork"]:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
    elif animal in ["cat","meow","pussy"]:
        contents = requests.get('http://aws.random.cat/meow').json()
        url = contents['file']
    elif animal in ["panda"]:
        contents = requests.get('https://some-random-api.ml/pandaimg').json()
        url = contents['link']
    elif animal in ["redpanda"]:
        contents = requests.get('https://some-random-api.ml/redpandaimg').json()
        url = contents['link']
    elif animal in ["pika","pikachu"]:
        contents = requests.get('https://some-random-api.ml/pikachuimg').json()
        url = contents['link']
    elif animal in ["fox"]:
        contents = requests.get('https://some-random-api.ml/foximg').json()
        url = contents['link']
    
    
    elif animal == "movingcat":
        import random
        num = str(random.randint(1,100000))
        url = "https://cataas.com/cat/gif?lol"+num
    return url


def animal_handler(bot, update, msg_list):
    if len(msg_list) > 1:
        animal = msg_list[1]
        url = get_image_url(animal)
        chat_id = update.message.chat_id
        bot.send_photo(chat_id=chat_id, photo=url)

        
        