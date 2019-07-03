from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

def fun_handler(bot, update, msg_list):
    if msg_list[1] in ["joke","roast","mock"]:
        if len(msg_list) > 2:
            fname = msg_list[2]
            lname = msg_list[3] if len(msg_list) > 3 else ""
        else:
            fname, lname = update.message.from_user.first_name, update.message.from_user.last_name
        contents = requests.get('http://api.icndb.com/jokes/random?firstName='+fname+'&lastName='+lname).json()
        url = contents['value']['joke']
        update.message.reply_text(url)

    elif msg_list[1] in ["google"]:
        link = "http://lmgtfy.com/?q=" + "+".join(msg_list[2:])
        update.message.reply_text(link)

    elif msg_list[1] in ["meme"]:
        contents = requests.get('https://some-random-api.ml/meme').json()
        url = contents['image']
        bot.send_photo(chat_id=update.message.chat_id, photo=url)

    
    elif msg_list[1] in ["quote"]:
        import re
        contents = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1').json()
        text = re.sub('<[^<]+?>', '', contents[0]["content"] + "\n -- " + contents[0]["title"])
        update.message.reply_text("`"+text+"`", parse_mode=telegram.ParseMode.MARKDOWN)
    
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
        bot.send_photo(chat_id=update.message.chat_id, photo="https://source.unsplash.com/random?"+ msg_list[2] +"&sig="+num)

    elif msg_list[1] in ["wink"]:
        contents = requests.get("https://some-random-api.ml/animu/wink").json()
        bot.send_animation(chat_id=update.message.chat_id, animation=contents["link"])


    elif msg_list[1] in ["die", "kill"]:
        import random
        ways_to_die = ["died in the sewer.", "ate a tube of superglue", "sold both the kidneys on the internet.", "Kept a rattle snake as a pet, which bit them.", "got sat on by an elephant.", "fell into elephant shit.", "drank horse piss and said yum.", "disturbed a nest of wasps for no good reason, got stung.", "took their helmet off in outer space.", "ate a two week old unrefridgerated pie.", "set fire to their hair.", "asked milan how to use git and got aws advice.", "held the door, HODOR.", "saw their face in the mirror, and felt a need to make it go away."]
        way_to_die = ways_to_die[random.randint(0,len(ways_to_die)-1)]
        if len(msg_list) == 2:
            uname = update.message.from_user.username
        else:
            uname = msg_list[2].replace("@","")
        update.message.reply_text(uname + " " + way_to_die)