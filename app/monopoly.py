from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import datetime
import random
import _thread
import time
from app.use import use_handler
from app.db import *

from app.utils import *


# the username can only be initialised by user
def check_mono_initialized(chat_id,username):
    create_user(chat_id, username)

def deduct_money_wrapper(chat_id,username,money):
    if money<0: return False
    user = get_user(chat_id, username)
    if has_active_debitcard(chat_id, username):
        if user["wallet"] >= money:
            deduct_money(chat_id, username, wallet = money)
        elif user["wallet"] + user["bankbalance"] >= money + int(money*0.05):
            money += int(money*0.005)
            deduct_money(chat_id, username, wallet = user["wallet"], bank=money-user["wallet"])
        else:
            return False
    else:   # doesnt have debit card
        if user["wallet"] >= money:
            deduct_money(chat_id, username, wallet = money)
        else:
            return False
    return True


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
            wallet = int(u['wallet'])
            bankbalance = int(u["bankbalance"])
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
        if "last_beg" in user:
            if not (datetime.datetime.today() - user["last_beg"]).seconds > 10:
                update.message.reply_text("You're begging too much. Stop it!! (wait %d seconds)" % \
                                    (10-int((datetime.datetime.today() - user["last_beg"]).seconds)))
                return
        
        beg_from = choose_random(load_replies("donators"))
        beg_line = choose_random(load_replies("beg_lines"))
        
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
        money = random.randint(20,100)
        user["last_search"] = datetime.datetime.today()
        update_user(user)
        add_money(chat_id, username, money)

        search_string = choose_random(load_replies("search_lines"))
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
                if deduct_money_wrapper(chat_id, username, money=100):
                    update.message.reply_text("You have successfully participated in the lottery.")
                    buy_lottery(chat_id, username)
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
            return

        if deduct_money_wrapper(chat_id, username, money):
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
            if money < 1 or money > user["wallet"]:
                update.message.reply_text("You dont have enough money to gamble.")
                return

        
        game = random.choice([True, True, True, False, False])
        multiplier =  float(random.randint(80,100) /100)

        if game:  # win
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
        item_str = "*Shop Items :*`\n" 
        for item in shop:
            item_str += item["name"] + " = " + str(item["price"]) + "\n"
        item_str += "`"
        # update.message.reply_text(item_str)
        bot.send_message(chat_id=chat_id, 
        text=item_str, 
        parse_mode=telegram.ParseMode.MARKDOWN)



    # pls buy coke
    elif msg_list[1] in ["buy", "purchase"]:

        item_name = msg_list[2]
        shop_item = get_shop_item(item_name)
        if shop_item:
            # limited items
            if "limit" in shop_item:
                if shop_item["limit"] <= get_item_quantity(chat_id, username, item_name):
                    update.message.reply_text("You can only buy " + str(shop_item["limit"]) + " " + item_name)
                    return

            if deduct_money_wrapper(chat_id, username, shop_item["price"]):
                expiry = shop_item["expiry"] if "expiry" in shop_item else None
                # deduct_money(chat_id, username, shop_item["price"])
                add_item_inventory(chat_id, username, item_name, shop_item["price"], expiry=expiry)
                update.message.reply_text("Item " + item_name + " has been purchased")                
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
            items_str = "*Inventory Items for "+ username +" :*`\n"
            for item in inventory:

                if item_has_expired(chat_id, username, item["name"]):
                    remove_item_inventory(chat_id, username, item["name"])
                    update.message.reply_text(item["name"] + " has expired.")
                    continue
                
                items_str += item["name"] + "("+ str(item["quantity"]) +") = " + str(item["price"]) + "\n"
            items_str +="`"
            # update.message.reply_text(items_str)

            bot.send_message(chat_id=chat_id, 
                text=items_str, 
                parse_mode=telegram.ParseMode.MARKDOWN)
    

    # pls use apple
    # pls use cake 
    elif msg_list[1] in ["use"]:
        if get_item_quantity(chat_id, username, msg_list[2]) == 0:
            update.message.reply_text("Item not in inventory")
        else:
            if item_has_expired(chat_id, username, msg_list[2])==False:
                use_handler(bot, update, msg_list)
            else:
                update.message.reply_text(msg_list[2] + " has expired.")
            remove_item_inventory(chat_id, username, msg_list[2])





    elif msg_list[1] in ["loan"]:
        if len(msg_list) == 2:
            loan = get_loan(chat_id, username)
            if loan:
                money = loan["amount"]
                time_period = int(( datetime.datetime.today() - loan["takenat"]).total_seconds() / 3600)
                interest = int(money*time_period*0.0005)
                update.message.reply_text("Loan :\nAmount: " + str(money) + "\nInterest : " + \
                            str(interest) + "\n Time Period : " + str(time_period) + "hrs")
            else:
                update.message.reply_text("You haven't taken any loans.")
        
        elif msg_list[2] in ["return","repay", "pay"]: 
            loan = get_loan(chat_id, username)
            if loan:
               
                money = loan["amount"]
                # interest every hr
                time_period = int(( datetime.datetime.today() - loan["takenat"]).total_seconds() / 3600)
                total_amount = int(money + int((money*time_period)*0.0005))
                repay_amount = total_amount
                if len(msg_list) == 4:
                    repay_amount = int(msg_list[3])
                
                if deduct_money_wrapper(chat_id, username, repay_amount):
                    revise_loan(chat_id, username, total_amount - repay_amount)
                    if repay_amount == total_amount:
                        update.message.reply_text("You cleared your loan.")
                    else:
                        update.message.reply_text("You paid part of your loan.")
                else:
                    update.message.reply_text("You need " + str(repay_amount) + " in your wallet/bank.")
            else:
                update.message.reply_text("You haven't taken any loans.")
            
        else:   # get loan
            money = int(msg_list[2])
            loan = get_loan(chat_id, username)
            if not loan:
                if money > 0 and money <= 100000:
                    take_loan(chat_id, username, money)
                    add_money(chat_id, username, money)
                    update.message.reply_text("You took a loan for " + str(money))    
                else:
                    update.message.reply_text("Please enter a value between 1 and 100000.")    
            else:
                update.message.reply_text("You already have an outstanding loan.")
                return

    elif msg_list[1] in ["bankrob"]:

        def start_robbery_countdown(user):
            time.sleep(10000)
            prob_dist = [True, False, False]
            robbers = get_bank_robbers(chat_id, user)
            if len(robbers) > 1:
                prob_dist.append(True)
                prob_dist.append(True)
            
            win = choice(prob_dist)
            if win:
                u = get_user(chat_id, user)
                bank_balance = u["bankbalance"]
                rob_amount = randint(1, bank_balance)
                share_amount = rob_amount/len(robbers)
                for robber in robbers:
                    add_money(chat_id, robber, wallet = share_amount)
                update.message.reply_text(user + " was robbed of " + str(rob_amount) + " by " + ", ".join(robbers)) + "."
                
            else:
                for robber in robbers:
                    r = get_user(chat_id, robber)
                    robber_w,robber_b = r["wallet"], r["bankbalance"]
                    set_money(chat_id, robber, robber_w/2, robber_b/2)
                    add_money(chat_id, user, wallet= (r["wallet"] + r["bankbalance"] )/4)
                update.message.reply_text(", ".join(robbers) + " were caught while robbing " + user + ". They lost half their money to " + user)
            rob_finish(chat_id, user)
            return

        # username
        to_user = msg_list[2].replace("@","")

        robbers = get_bank_robbers(chat_id, to_user)
        if robbers:
            rob_bank(chat_id, username, to_user)
            update.message.reply_text("Joined robbery.")
        else:
            rob_bank(chat_id, username, to_user)
            update.message.reply_text("10s until robbery.")
            _thread.start_new_thread( start_robbery_countdown, (to_user, ) )
            return

