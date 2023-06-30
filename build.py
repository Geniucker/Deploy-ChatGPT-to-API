#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from subprocess import getoutput, Popen, PIPE
import os
import sys
import run
import time

def ERROR(msg):
    print("\033[31m[ERROR]\033[0m" + msg)

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
    ERROR("Please install git first.")
    input("Press enter to exit...")
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
    print("Try to update ChatGPT-to-API...")
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
    print("- {}".format(i))
print()

while "continue" != input("type continue to continue:"):
    pass


# build in docker
if choice == "1":
    if not testCMD("docker"):
        ERROR("Please install docker first.")
        input("Press enter to exit...")
        exit(1)

    # set proxy
    with open("Dockerfile_template", "r") as f:
        dockerfile = f.read()
    if run.proxy != "":
        with open("Dockerfile", "w") as f:
            if run.proxy.split(":")[0] in ["127.0.0.1", "localhost", "::1"]:
                proxy = "host.docker.internal:{}".format(run.proxy.split(":")[1])
            else:
                proxy = run.proxy
            f.write(
                dockerfile.format(
                    "ENV http_proxy {}://{}".format(run.proxy_type, proxy),
                    "ENV https_proxy {}://{}".format(run.proxy_type, proxy)
                )
            )
    else:
        with open("Dockerfile", "w") as f:
            f.write(dockerfile.format("", ""))

    os.system("docker compose down")
    if getoutput("docker image ls").find("chatgpttoapi") != -1:
        os.system("docker image rm chatgpttoapi")
    os.system("docker compose build")

# build in host
elif choice == "2":
    if not testCMD("go"):
        ERROR("Please install go first.")
        input("Press enter to exit...")
        exit(1)

    # set proxy
    if run.proxy != "":
        os.environ["https_proxy"] = run.proxy
        os.environ["http_proxy"] = run.proxy

    os.chdir("ChatGPT-to-API")
    os.system("go build")
    if sys.platform.find("win32") != -1:
        os.system("copy freechatgpt.exe ..")
    else:
        os.system("cp freechatgpt ..")
    os.chdir("../Authenticatior")
    os.system("go build")
    if sys.platform.find("win32") != -1:
        os.system("copy authentication.exe ..")
    else:
        os.system("cp authentication ..")


input("Build finished. Press enter to exit...")
