from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

def fun_handler(bot, update, msg_list):
    if msg_list[1] in ["joke","roast","mock"]:
        if len(msg_list) > 2:
            fname = msg_list[2]
            lname = msg_list[3] if len(msg_list) > 3 else ""
        else:
            fname, lname = update.message.from_user.first_name, update.message.from_user.last_name
        print(fname,lname)
        contents = requests.get('http://api.icndb.com/jokes/random?firstName='+fname+'&lastName='+lname).json()
        url = contents['value']['joke']
        update.message.reply_text(url)

    elif msg_list[1] in ["google"]:
        link = "http://lmgtfy.com/?q=" + "+".join(msg_list[2:])
        update.message.reply_text(link)

    elif msg_list[1] in ["meme"]:
        contents = requests.get('https://some-random-api.ml/meme').json()
        url = contents['url']
        bot.send_photo(chat_id=update.message.chat_id, photo=url)
    
    elif msg_list[1] in ["quote"]:
        import re
        contents = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1').json()
        text = re.sub('<[^<]+?>', '', contents[0]["content"] + "\n -- " + contents[0]["title"])
        update.message.reply_text(text)
    
    elif msg_list[1] in ["xkcd"]:
        import random
        num = str(random.randint(1,2120))
        contents = requests.get('https://xkcd.com/'+num+'/info.0.json').json()
        url = contents["img"]
        bot.send_photo(chat_id=update.message.chat_id, photo=url)

    elif msg_list[1] in ["geek","geekjoke"]:
        contents = requests.get("https://geek-jokes.sameerkumar.website/api").text
        update.message.reply_text(contents)

    elif msg_list[1] in ["dice"]:
        import random
        num = random.randint(1,6)
        update.message.reply_text("Dice : " + str(num))

    elif msg_list[1] in ["coin","flip"]:
        import random
        num = random.randint(1,2)
        txt = "Heads!"
        if num == 2: txt = "Tails!"
        update.message.reply_text(txt)

    elif msg_list[1] in ["choose","select"]:
        import random
        item_list=msg_list[2:]
        num =random.randint(0,len(item_list)-1)
        update.message.reply_text(item_list[num])

    elif msg_list[1] in ["avatar"]:
        if len(msg_list) > 2:
            username = msg_list[2].replace("@","")
        else:
            username = update.message.from_user.username
        bot.send_photo(chat_id=update.message.chat_id, photo="https://api.adorable.io/avatars/285/"+ username +"@adorable.io.png")


    elif msg_list[1] in ["unsplash","wall","wallpaper"]:
        import random
        num = str(random.randint(1,100000000))
        bot.send_photo(chat_id=update.message.chat_id, photo="https://source.unsplash.com/random?random&cat&time="+num)