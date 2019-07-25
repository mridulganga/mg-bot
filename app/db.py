import pymongo
import datetime
import os

# mongo_creds = open("api/mongo","r")
# client = pymongo.MongoClient(mongo_creds.read())

client = pymongo.MongoClient(os.environ["MONGO"])
db = client.main

def init():
    for collection in ["chats","users","shop","polls","todos","inventory", "loans"]:
        try:
            db.create_collection(collection)
        except pymongo.errors.CollectionInvalid:
            pass



############################
#   CHAT
############################

def create_chat_id(chat_id):
    o = db.chats.find_one({"chat_id" : str(chat_id)})
    if o==None:
        return db.chats.insert_one({"chat_id":str(chat_id)}).inserted_id
    else:
        return o["_id"]

def get_chat(chat_id):
    return db.chats.find_one({"chat_id" : str(chat_id)})

def update_chat(chat):
    o = db.chats.find_one_and_replace({"_id":chat["_id"]}, chat)



############################
#   USERS AND USER
############################

def get_users(chat_id):
    return db.users.find({"chat_id":str(chat_id)})

def get_user(chat_id,username):
    username = username.lower()
    return db.users.find_one({
        "$and":[ {"username":username}, {"chat_id":str(chat_id)}]
    })
    

def update_user(new_obj):
    o = db.users.find_one_and_replace({"_id":new_obj["_id"]},new_obj)

def create_user(chat_id, username):
    # create chat id 
    create_chat_id(chat_id)
    # get user if exists otherwise create and get
    user = get_user(chat_id,username)
    if not user:
        db.get_collection("users").insert_one({
            "username": username,
            "wallet" : 0,
            "bankbalance" : 0,
            "chat_id" : str(chat_id),
        })
    user = get_user(chat_id,username)
    return user
    


############################
#   MONEY AND BALANCE
############################

def add_money(chat_id, username, wallet=-1, bank=-1):
    user = get_user(chat_id,username)
    if wallet != -1: user["wallet"] += wallet
    if bank != -1: user["bankbalance"] += bank
    update_user(user)

def deduct_money(chat_id, username, wallet=-1, bank=-1):
    user = get_user(chat_id,username)
    if wallet != -1: user["wallet"] -= wallet
    if bank != -1: user["bankbalance"] -= bank
    update_user(user)

def set_money(chat_id, username, wallet=-1, bank=-1):
    user = get_user(chat_id, username)
    if wallet != -1:  user["wallet"] = wallet
    if bank != -1:  user["bankbalance"] = bank
    update_user(user)

def withdraw_money(chat_id, username, money):
    user = get_user(chat_id, username)
    if money > 0:
        user["wallet"] += money
        user["bankbalance"] -= money
        update_user(user)

def deposit_money(chat_id, username, money):
    user = get_user(chat_id, username)
    if money > 0:
        user["wallet"] -= money
        user["bankbalance"] += money
        update_user(user)



############################
#   LOTTERY
############################
def get_lottery_users(chat_id):
    chat = get_chat(chat_id)
    if "lottery" in chat:
        return chat["lottery"]
    else:
        return []


def buy_lottery(chat_id, username):
    chat = get_chat(chat_id)
    if "lottery" in chat:
        chat["lottery"].append(username)
        update_chat(chat)
    else:
        chat["lottery"] = [username]
        update_chat(chat)

def clear_lottery(chat_id):
    chat = get_chat(chat_id)
    if "lottery" in chat:
        chat.pop("lottery")
        update_chat(chat)





############################
#   TO DO
############################
def add_todo(chat_id, todo):
    db.todos.insert_one({
        "todo" : todo,
        "chat_id" : str(chat_id)
    })

def get_todos(chat_id):
    return db.todos.find({"chat_id":str(chat_id)})

def remove_todo(chat_id, todo_number):
    todos = get_todos(chat_id)
    c = 1
    for todo in todos:
        if c == todo_number:
            db.todos.remove({"_id":todo["_id"]})
        c+=1

def clear_todos(chat_id):
    db.todos.delete_many({'chat_id': str(chat_id)})




############################
#   POLL
############################

def create_poll(chat_id, question, options):
    end_poll(chat_id)
    db.polls.insert_one({
        "question" : question,
        "options" : options,
        "chat_id" : str(chat_id)
    })

def end_poll(chat_id):
    db.polls.delete_many({"chat_id": str(chat_id)})

def update_poll(poll):
    db.polls.find_one_and_replace({"_id":poll["_id"]},poll)

def vote_poll(chat_id, username, vote_num):
    poll = db.polls.find_one({"chat_id" : str(chat_id)})
    if poll:
        if "votes" in poll:
            poll["votes"][username] = vote_num
            update_poll(poll)
        else:
            poll["votes"] = {username:vote_num}
            update_poll(poll)
    else:
        return None

def get_poll_options(chat_id):
    poll = db.polls.find_one({"chat_id" : str(chat_id)})
    return poll["options"]

def get_votes(chat_id):
    poll = db.polls.find_one({"chat_id":str(chat_id)})
    
    def getKeysByValue(dictOfElements, valueToFind):
        listOfKeys = list()
        listOfItems = dictOfElements.items()
        for item  in listOfItems:
            if item[1] == valueToFind:
                listOfKeys.append(item[0])
        return  listOfKeys
    
    votes = []
    for option in poll["options"]:
        i = poll["options"].index(option) + 1
        users = getKeysByValue(poll["votes"],i)
        votes.append((i,option,users))

    return votes



def get_shop_items():
    return db.shop.find()

def get_shop_item(item_name):
    return db.shop.find_one({"name":item_name})

def get_inventory(chat_id, username):
    return db.inventory.find({
        "$and" : [{"chat_id" : str(chat_id)},{"username" : username}]
    })

def get_item_inventory(chat_id, username, item_name):
    return db.inventory.find_one({
        "$and" : [{"chat_id" : str(chat_id)},{"username" : username}, {"name" : item_name}]
    })

def save_item_intentory(item):
    db.inventory.find_one_and_replace({"_id":item["_id"]},item)

def add_item_inventory(chat_id, username, item_name, price, expiry=None):
    inventory = get_inventory(chat_id, username)
    if inventory:
        item = get_item_inventory(chat_id, username, item_name)
        if not item:
            item = {
                "name" : item_name,
                "quantity" : 1,
                "price" : price,
                "chat_id" : str(chat_id),
                "username" : username
            }
            if expiry: item["expiry"] = datetime.datetime.today() + datetime.timedelta(seconds=expiry) 
            db.inventory.insert(item)
        else:
            item["quantity"] +=1
            save_item_intentory(item)

def get_item_quantity(chat_id, username, item_name):
    item = get_item_inventory(chat_id, username, item_name)
    if not item:
        return 0
    else:
        return int(item["quantity"])

def remove_item_inventory(chat_id, username, item_name):
    item = get_item_inventory(chat_id, username, item_name)
    if item:
        if item["quantity"] == 1:
            db.inventory.remove({
                "$and" : [{"chat_id" : str(chat_id)}, {"username" : username}, {"name" : item_name}]
            })
        else:
            item["quantity"] -=1
            save_item_intentory(item)





def get_loan(chat_id, username):
    return db.loans.find_one({
        "$and" : [{"chat_id":str(chat_id)},{"username":username}]
    })

def clear_loan(chat_id, username):
    db.loans.remove({
        "$and" : [{"chat_id":str(chat_id)},{"username":username}]
    })

def take_loan(chat_id, username, amount):
    import datetime
    db.loans.insert_one({
        "amount" : amount,
        "takenat" : datetime.datetime.today(),
        "chat_id" : str(chat_id),
        "username" : username
    })


init()