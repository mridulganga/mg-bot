
help_dict = {
    # monopoly help
    ("monopoly",) : "*Monopoly Commands*:\n`balance, search, beg, daily, buy, sell, use, shop, inventory, deposit, withdraw, lottery, gamble, share, rich, lootbox, loan`",
    ("balance",)  :     "`pls balance\npls balance @username`  \nView bank and Wallet balance",
    ("search",)  :      "`pls search`  \nSearch for money",
    ("beg",)  :         "`pls beg`     \nBeg for money",
    ("daily",)  :       "`pls daily`   \nGet 200-300 daily",
    ("shop",)  :        "`pls shop`    \nView items in shop",
    ("buy",)  :         "`pls buy item`   \nBuy an item from shop ",
    ("sell",)  :        "`pls sell item`  \nSell item from inventory to get money back",
    ("inventory",)  :   "`pls inventory`  \nView your inventory items",
    ("deposit",)  :     "`pls deposit 100\npls deposit all` \nDeposit money from wallet to bank",
    ("withdraw",)  :    "`pls withdaw 100\npls withdraw all` \nWithdraw money from bank to wallet",
    ("steal",)  :       "`pls steal @username`   \nSteal money from @user if they have more than 200",
    ("share",)  :       "`pls share @username 100`   \nShare money to @user",
    ("gamble",)  :      "`pls gamble all\npls gamble 100`    \nGamble money (win/lose)",
    ("lottery",)  :     "`pls lottery view\npls lottery buy\npls lottery results`    \nBuy lottery tickets and see results",
    ("loan",)  :        "Loan Help*:\n`pls loan        -view loan status\npls loan 5000   -get loan of 5000\npls loan pay    -repay loan`",
    ("lootbox",)  :     "`pls buy lootbox100\npls use lootbox100`    \nbuy lootboxes and use them to get rewards",
    ("rich",)  :        "`pls rich`  \nShow list of rich people in the group",


    ("poll",) : "*Poll Usage*:\n`pls poll      -create new poll\npls vote 2    -vote for 2nd option\npls vote      -show poll votes\npls vote end  -end poll and show results`",
    ("vote",) : "`pls vote 2\npls vote end`",

    ("todo",) : "*Todo Usage*:\n`pls todo           -list todos\npls todo item      -add todo \npls todo remove 2  -remove 2nd item\npls todo remove    -remove everything\n`",

    ("fun",) : "*Fun Commands*:\n`joke, google, meme, quote, xkcd, geek, coin, dice, avatar, unsplash`",
    ("choose",) : "*Choose*:\n`pls choose item1 item2 item3`",
    ("animals",) : "*Animals*:\n`dog, cat, panda, fox, redpanda, pika`\nUsage :\n`pls meow\npls bork`"
}

def get_help(query):
    i = query
    for x in help_dict:
        if i in x:
            return "*HELP*:\n" + help_dict[x]
    return "Cant help you with that, sorry!"