#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from subprocess import getoutput, Popen, PIPE
import os
import sys
import run
import time


def testCMD(cmd:str):
    cmd = cmd.split(" ")[0]
    check = False

    if sys.platform.find("win32") != -1:
        if ".exe" != cmd[-4:]:
            cmd += ".exe"
        path = os.environ["PATH"].split(";")
        for i in path:
            if os.path.exists("{}\\{}".format(i, cmd)):
                check = True
                break
    else:
        path = os.environ["PATH"].split(":")
        for i in path:
            if os.path.exists("{}/{}".format(i, cmd)):
                check = True
                break
    return check


if not testCMD("git"):
    print("Please install git first.")
    time.sleep(3)
    exit(1)

if not os.path.exists("ChatGPT-to-API"):
    choice = ""
    while choice not in ["1", "2"]:
        choice = input(
    """Which method do you want to clone ChatGPT-to-API?
    1. https (you may need to setup proxy for git)
    2. ssh (if you have set up ssh key, ssh is recommended)"""
        )
    if choice == "1":
        os.system("git clone https://github.com/Geniucker/ChatGPT-to-API.git")
    elif choice == "2":
        os.system("git clone git@github.com:Geniucker/ChatGPT-to-API.git")
else:
    os.system("cd ChatGPT-to-API && git pull && cd ..")

choice = ""
while choice not in ["1", "2"]:
    choice = input(
"""Which method do you want to use?
1. Run in docker
2. Run in host
"""
    )

print("Please modify the variable \"proxy\", \"proxy_type\", \"accounts\", \"server_host\", \"server_port\" in run.py")
while "continue" != input("type continue to continue: "):
    pass

print("Your proxy is: {}".format(run.proxy))
print()
print("your accounts are:")
for i in run.accounts:
    print("- {}:{}".format(i, run.accounts[i]))
print()

while "continue" != input("type continue to continue:"):
    pass

# set proxy
os.environ["HTTPS_PROXY"] = run.proxy
os.environ["HTTP_PROXY"] = run.proxy

if choice == "1":
    if not testCMD("docker"):
        print("Please install docker first.")
        time.sleep(3)
        exit(1)
    os.system("docker compose down")
    if getoutput("docker image ls").find("chatgpttoapi") != -1:
        os.system("docker image rm chatgpttoapi")
    os.system("docker compose build")
    os.system("docker compose up -d")
elif choice == "2":
    os.chdir("ChatGPT-to-API")
    if not testCMD("go"):
        print("Please install go first.")
        time.sleep(3)
        exit(1)
    os.system("go build")
    os.system("cd tools/authenticator && go build && cd ../..")
    if sys.platform.find("win32") != -1:
        os.system("cp tools/authenticator/authenticator.exe ..")
        os.system("cp freechatgpt.exe ..")
    else:
        os.system("cp tools/authenticator/authenticator ..")
        os.system("cp freechatgpt ..")


input("Build finished. Press enter to exit...")
