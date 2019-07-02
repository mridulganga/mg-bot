import subprocess
import time
import requests

process = None

commit = None

def get_git_head():
    r = requests.get("https://github.com/mridulganga/mg-bot/commits/master")
    s = r.text.find("/mridulganga/mg-bot/commit/") + len("/mridulganga/mg-bot/commit/")
    e = r.text.find("\"",s)
    txt = r.text[s:e]
    return(txt)


def git_pull():
    p = subprocess.Popen("git pull origin master", shell=True)
    p.communicate()
    

def start_program():
    print("bot process starting")
    process = subprocess.Popen("python3 main.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


while(True):
    if get_git_head() != commit:
        commit = get_git_head()
        if process:
            print("bot process killing")
            process.kill()
        git_pull()
        start_program()

    time.sleep(5)