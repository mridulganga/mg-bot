
help_dict = {
    # monopoly help
    ("monopoly",) : "*Monopoly Commands*:\n`balance,daily,buy,sell,steal, shop, market, store, buy, purchase, sell, inventory, balance, deposit, withdraw, lottery, gamble, share, send, steal, rich, beg`",
    ("balance",) : "`pls balance\npls balance @username`",
    ("deposit",) : "`pls deposit 100\npls deposit all`",
    ("withdraw",) : "`pls withdaw 100\npls withdraw all`",
    ("steal",) : "`pls steal @username`",
    ("share","send") : "`pls share @username 100`",
    ("gamble",) : "`pls gamble all\npls gamble 100`",
    ("beg",) : "`pls beg`",
    ("lottery",) : "`pls lottery view\npls lottery buy\npls lottery results`",


    ("poll",) : "*Poll Usage*:\n`pls poll      -create new poll\npls vote 2    -vote for 2nd option\npls vote      -show poll votes\npls vote end  -end poll and show results`",
    ("vote",) : "`pls vote 2\npls vote end`",

    ("todo",) : "*Todo Usage*:\n`pls todo           -list todos\npls todo item      -add todo \npls todo remove 2  -remove 2nd item\npls todo remove    -remove everything\n`"
}

def get_help(query):
    i = query
    for x in help_dict:
        if i in x:
            return "*HELP*:\n" + help_dict[x]
    return "Cant help you with that, sorry!"