import subprocess
import time
import requests

process = None

commit = None

def get_git_head():
    r = requests.get("https://api.github.com/repos/mridulganga/mg-bot/commits/master")
    print(r.json())
    lcommit = r.json()["sha"]
    return lcommit


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