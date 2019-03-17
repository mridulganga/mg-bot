from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
from app.use import use_handler
from app.db import *



# the username can only be initialised by user
def check_mono_initialized(chat_id,username):
    create_user(chat_id, username)


def mono_handler(bot, update, msg_list):
    chat_id = update.message.chat_id
    try:
        username = update.message.from_user.username.lower()
    except:
        update.message.reply_text("Please goto Telegram Settings and add your username.")
        return
    
    # Check if the monopoly has been initialised. (the chat_id and/or the username)
    check_mono_initialized(chat_id, username)

    # user = mono[chat_id]["users"][username]
    user = get_user(chat_id, username)


    # pls balance
    # pls deposit 100
    # pls withdraw 500
    # View the balance for User
    if msg_list[1] in ["balance"]:
        if len(msg_list) > 2: username = msg_list[2].replace("@","") 
        u = get_user(chat_id, username)
        if u:
            wallet = u['wallet']
            bankbalance = u["bankbalance"]
            update.message.reply_text("Balance Information: \n Wallet: "+ str(wallet) + "\n Bank: " + str(bankbalance) )
        else:
            update.message.reply_text("User doesn't exist.")



    # pls deposit all
    # pls deposit 200
    elif msg_list[1] in ["deposit"]:
        if len(msg_list) == 2 or msg_list[2] == "all":
            # user["bankbalance"] += user["wallet"]
            # user["wallet"] = 0
            deposit_money(chat_id, username, user["wallet"])
            update.message.reply_text("All your money is deposited.")
        else:
            money = int(msg_list[2])
            if money <= user["wallet"]:
                # user["bankbalance"] += money
                # user["wallet"] -= money
                deposit_money(chat_id, username, money)
                update.message.reply_text(str(money) + " has been deposited.")
            else:
                update.message.reply_text("You dont have that kind of money in your wallet.")
        


    # pls withdraw all
    # pls withdraw 200
    elif msg_list[1] in ["withdraw"]:
        if len(msg_list) == 2 or msg_list[2] == "all":
            # user["wallet"] += user["bankbalance"]
            # user["bankbalance"] = 0 
            withdraw_money(chat_id, username, user["bankbalance"])
            update.message.reply_text("All your money is withdrawn.")
        else:
            try:
                money = int(msg_list[2])
            except:
                update.message.reply_text("Please Enter a numeric value or all.")
                return
            if money <= user["bankbalance"]:
                # user["wallet"] += money
                # user["bankbalance"] -= money
                withdraw_money(chat_id, username, money)
                update.message.reply_text(str(money) + " has been withdrawn.")
            else:
                update.message.reply_text("You dont have that kind of money in your bank.")



    # pls beg
    # beg timer = 10s
    elif msg_list[1] in ["beg"]:
        import random
        if "last_beg" in user:
            if not (datetime.datetime.today() - user["last_beg"]).seconds > 10:
                update.message.reply_text("You're begging too much. Stop it!! (wait %d seconds)" % \
                                    (10-int((datetime.datetime.today() - user["last_beg"]).seconds)))
                return
        donators = ["Liam", "Noah", "William", "James", "Logan", "Benjamin", "Mason", "Elijah", "Oliver", "Jacob", "Lucas", "Michael", "Alexander", "Ethan", "Daniel", "Matthew", "Aiden", "Henry", "Joseph", "Jackson", "Samuel", "Sebastian", "David", "Carter", "Wyatt", "Jayden", "John", "Owen", "Dylan", "Luke", "Gabriel", "Anthony", "Isaac", "Grayson", "Jack", "Julian", "Levi", "Christopher", "Joshua", "Andrew", "Lincoln", "Mateo", "Ryan", "Jaxon", "Nathan", "Aaron", "Isaiah", "Thomas", "Charles", "Caleb", "Josiah", "Christian", "Hunter", "Eli", "Jonathan", "Connor", "Landon", "Adrian", "Asher", "Cameron", "Leo", "Theodore", "Jeremiah", "Hudson", "Robert", "Easton", "Nolan", "Nicholas", "Ezra", "Colton", "Angel", "Brayden", "Jordan", "Dominic", "Austin", "Ian", "Adam", "Elias", "Jaxson", "Greyson", "Jose", "Ezekiel", "Carson", "Evan", "Maverick", "Bryson", "Jace", "Cooper", "Xavier", "Parker", "Roman", "Jason", "Santiago", "Chase", "Sawyer", "Gavin", "Leonardo", "Kayden", "Ayden", "Jameson", "Kevin", "Bentley", "Zachary", "Everett", "Axel", "Tyler", "Micah", "Vincent", "Weston", "Miles", "Wesley", "Nathaniel", "Harrison", "Brandon", "Cole", "Declan", "Luis", "Braxton", "Damian", "Silas", "Tristan", "Ryder", "Bennett", "George", "Emmett", "Justin", "Kai", "Max", "Diego", "Luca", "Ryker", "Carlos", "Maxwell", "Kingston", "Ivan", "Maddox", "Juan", "Ashton", "Jayce", "Rowan", "Kaiden", "Giovanni", "Eric", "Jesus", "Calvin", "Abel", "King", "Camden", "Amir", "Blake", "Alex", "Brody", "Malachi", "Emmanuel", "Jonah", "Beau", "Jude", "Antonio", "Alan", "Elliott", "Elliot", "Waylon", "Xander", "Timothy", "Victor", "Bryce", "Finn", "Brantley", "Edward", "Abraham", "Patrick", "Grant", "Karter", "Hayden", "Richard", "Miguel", "Joel", "Gael", "Tucker", "Rhett", "Avery", "Steven", "Graham", "Kaleb", "Jasper", "Jesse", "Matteo", "Dean", "Zayden", "Preston", "August", "Oscar", "Jeremy", "Alejandro", "Marcus", "Dawson", "Lorenzo", "Messiah", "Zion", "Maximus"]
        beg_lines = ["go buy some food", "go gamble it", "go smoke some weed", "go eat some muffins", "go cry in the corner", "go buy some clothes", "go spend it wisely", "go get a life"]
        
        beg_from = donators[random.randint(0,len(donators)-1)]
        beg_line = beg_lines[random.randint(0,len(beg_lines)-1)]
        
        beg_amount = random.randint(10,100)
        user["last_beg"] = datetime.datetime.today()
        update_user(user)
        add_money(chat_id, username, beg_amount)
        update.message.reply_text(beg_from + " donated " + str(beg_amount) + " " + beg_line)


    # pls daily
    # daily timer = 1 day
    elif msg_list[1] in ["daily"]:
        if "last_daily" in user:
            diff_time = (datetime.datetime.today() - user["last_daily"])
            if diff_time.days < 1:
                diff_time = datetime.timedelta(days=1) - diff_time
                time_left = str(diff_time.seconds//3600) + "hrs and " + str((diff_time.seconds//60)%60) + "mins"
                update.message.reply_text("You have already gotten your share for the day, try again after " + time_left)
                return
        import random
        money = random.randint(200,300)
        user["last_daily"] = datetime.datetime.today()
        update_user(user)
        add_money(chat_id, username, money)
        update.message.reply_text("You got %d for the day, spend it wisely." % money)
        

    # pls search
    # search timer = 10s
    elif msg_list[1] in ["search"]:
        if "last_search" in user:
            if (datetime.datetime.today() - user["last_search"]).seconds < 10:
                update.message.reply_text("You need to wait "+ str(10-(datetime.datetime.today() - user["last_search"]).seconds) +"s to continue searching.")
                return
        import random
        money = random.randint(20,100)
        user["last_search"] = datetime.datetime.today()
        update_user(user)
        add_money(chat_id, username, money)

        search_strings = ["under the sofa", "inside the hidden pocket", "inside the kitchen box", "inside the safe", "inside the boot of your vehicle", "inside the lunchbox", "behind your phone car", "inside your girlfriend's bag", "inside the flush tank", "inside your bong pot", "inside a random person's buttcrack", "inside the dimensions of space", "inside the Washing machine lint drawer", "inside your cat's litter box"]
        search_string = search_strings[random.randint(0,len(search_strings)-1)]
        update.message.reply_text("Congrats you found " + str(money) + " " + search_string)




    # pls lottery results
    # pls lottery buy
    # pls lottery view 
    elif msg_list[1] in ["lottery"]:
        
        lottery_users = get_lottery_users(chat_id)
        if msg_list[2] in ["buy"]:
            if username in lottery_users:   # participated already
                update.message.reply_text("You have already participated. Use \npls lottery results")
            else:   # participate in lottery
                if user["wallet"] >= 10:
                    deduct_money(chat_id, username, wallet = 10)
                    buy_lottery(chat_id, username)
                    update.message.reply_text("You have successfully participated in the lottery.")
                else:
                    update.message.reply_text("You dont even have enough money to buy a lottery ticket.")
                
        elif msg_list[2] in ["view"]:
            if len(lottery_users) > 0:
                update.message.reply_text("Lottery Participants :\n" + "\n".join(lottery_users))
            else:
                update.message.reply_text("No participants in lottery.")
        
        elif msg_list[2] in ["result","results"]:    
            num = len(lottery_users)
            money = 10 * num * num
            import random 
            winner = lottery_users[random.randint(0, len(lottery_users)-1)] # random select
            # u = get_user(chat_id, winner)
            add_money(chat_id, winner, wallet=money)
            clear_lottery(chat_id)
            update.message.reply_text(winner + " won the lottery. Prize money : " + str(money))




    # pls share @username 100
    # pls send @username 100
    elif msg_list[1] in ["share","send"]:
        if len(msg_list) == 2:
            update.message.reply_text("Please specify the user and amount, see \npls help share")
            return
        to_user = msg_list[2].replace("@","")
        try:
            money = int(msg_list[3])
        except:
            update.message.reply_text("Please enter a valid numeric amount.")

        if user["wallet"] > money and money > 0:
            deduct_money(chat_id, username, wallet=money)
            u = get_user(chat_id, to_user)
            add_money(chat_id, to_user, money)
            update.message.reply_text("Money has been sent.")
        else:
            update.message.reply_text("You dont have so much money to share.")



    # pls gamble all
    # pls gamble 50
    elif msg_list[1] in ["gamble"]:
        # check wallet status
        if msg_list[2] == "all":
            money = user["wallet"]
            if money < 1:
                update.message.reply_text("You dont have enough money to gamble.")
                return
        else:
            money = int(msg_list[2])
            if money < 2 or money > user["wallet"]:
                update.message.reply_text("You dont have enough money to gamble.")
                return

        import random
        game = random.randint(1,2)
        multiplier =  float(random.randint(80,100) /100)

        if game==2:  # win
            money = int(money * multiplier)
            add_money(chat_id, username, money)
            update.message.reply_text("Congrats!!\nYou won this round. You got " + str(money))
        else: # lose
            deduct_money(chat_id, username, money)
            update.message.reply_text("You lost this round.")




    # pls steal @username
    # need minumum 200
    elif msg_list[1] in ["steal"]:
        if len(msg_list) < 3:
            update.message.reply_text("Whom you wanna steal from?")
            return

        steal_from = msg_list[2].replace("@","")
        money = get_user(chat_id, steal_from)["wallet"]
        
        # check minimum 200 in either wallets
        if money < 200 or user["wallet"] < 200:
            update.message.reply_text("Both you and the victim should have minimun 200 in the wallet to steal.")
            return

        # success or got caught
        import random
        steal_or_not = random.randint(1,2)

        if steal_or_not == 2: # steal successfull
            how_much = random.randint(10,int(money/2))
            deduct_money(chat_id, steal_from, how_much)
            add_money(chat_id, username, how_much)
            update.message.reply_text("You were able to steal " + str(how_much) + " from " + steal_from)

        else: # caught
            how_much = random.randint(10,int(user["wallet"]/2))
            deduct_money(chat_id, username, how_much)
            add_money(chat_id, steal_from, how_much)
            update.message.reply_text("Damn! You got caught and paid " + str(how_much) + " to " + steal_from)





    # pls rich
    # list top 3 rich people
    elif msg_list[1] in ["rich"]:
        import pymongo
        rich_people = "Rich People : \n"
        users = get_users(chat_id).sort("wallet",pymongo.DESCENDING)
        for u in users:
            rich_people += u["username"] + "  ("+ str(u["wallet"]) +")\n"
        
        update.message.reply_text(rich_people)



    # pls shop
    elif msg_list[1] in ["shop", "market", "store"]:
        shop = get_shop_items()
        item_str = "Shop Items :\n"
        for item in shop:
            item_str += item["name"] + " = " + str(item["price"]) + "\n"
        update.message.reply_text(item_str)



    # pls buy coke
    elif msg_list[1] in ["buy", "purchase"]:

        item_name = msg_list[2]
        shop_item = get_shop_item(item_name)
        if shop_item:
            if shop_item["price"] <= user["wallet"]:
                add_item_inventory(chat_id, username, item_name, shop_item["price"])
                update.message.reply_text("Item " + item_name + " has been purchased")
                deduct_money(chat_id, username, shop_item["price"])
            else:
                update.message.reply_text("You dont have enough money.")
        else:
            update.message.reply_text("Item does not exist.")


    # pls sell coke
    elif msg_list[1] in ["sell"]:
        item_name = msg_list[2]
        inventory_item = get_item_inventory(chat_id, username, item_name)
        if not inventory_item:
            update.message.reply_text("Item not found in your inventory.")
        else:
            remove_item_inventory(chat_id, username, item_name)
            add_money(chat_id, username, inventory_item["price"])
            update.message.reply_text("Item has been sold.")



    # pls inventory
    # View the Items in the Shop
    elif msg_list[1] in ["inventory"]:
        inventory = get_inventory(chat_id, username)
        if inventory:
            items_str = "Inventory Items :\n"
            for item in inventory:
                items_str += item["name"] + "("+ str(item["quantity"]) +") = " + str(item["price"])
            update.message.reply_text(items_str)
    

    # pls use apple
    # pls use cake @username
    elif msg_list[1] in ["use"]:
        remove_item_inventory(chat_id, username, msg_list[2])
        use_handler(bot, update, msg_list)