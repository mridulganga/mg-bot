# Home for utility functions
import random

replies = {}

def load_replies(reply_key):
    global replies

    if reply_key in replies:
        return  replies[reply_key]
    else:
        f = open("data/"+reply_key, "r")
        key_replies = f.read().split("\n")
        f.close()
        replies[reply_key] = key_replies
        return key_replies

def choose_random(choose_from_list):
    reply = choose_from_list[random.randint(0,len(choose_from_list)-1)]
    return reply

def get_random_number():
    return str(random.randint(1,100000000000))