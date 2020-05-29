# mg-bot
mg bot for telegram. This bot was inspired by dankmemer bot from Discord.


To add this bot to your telegram group, look for `@themg_bot`.

### Features
- animal images
- fun and utils 
- monopoly game
- poll (not as good as telegram poll)
- todo list
etc


### Things to remember
- add username in your account to use monopoly
- the first bot command can take some time as server has sleep time
- use `pls help` to see the list of sections and help

### Tech
- python
- python-telegram-bot lib
- pymongo
- mongodb

### Run the bot locally
```
pip3 install -r requirements.txt

export TELEGRAM=<your telegram bot token>
export MONGO=<mongo db access url with creds>
export PORT=5000

python3 main.py local
```
