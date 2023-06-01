#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput, Popen, PIPE, STDOUT
import os
import sys

proxy = "localhost:7890"  # if you don't use proxy, set it to ""
proxy_type = "socks5"  # socks5 or http
accounts = {
    "user1": "password1",
    # "user2": "password2"
}
server_host = "0.0.0.0"
server_port = "8080"  # if deploy in docker, set it to "8080"


def ERROR(msg):
    print("\033[31m[ERROR]\033[0m" + msg)
def INFO(msg):
    print("\033[32m[INFO]\033[0m" + msg)
def WARNING(msg):
    print("\033[33m[WARNING]\033[0m" + msg)


if __name__=="__main__":
    if proxy.split(":")[0] in ["127.0.0.1", "localhost", "::1"] and os.path.exists("/.dockerenv"):
        proxy = "host.docker.internal:{}".format(proxy.split(":")[1])
    if proxy != "":
        os.environ["http_proxy"] = "{}://{}".format(proxy_type, proxy)
    os.environ["SERVER_HOST"] = server_host
    os.environ["SERVER_PORT"] = server_port
    os.environ["GIN_MODE"] = "release"
    while True:
        # config access_tokens
        with open("accounts.txt", "w") as f:
            for i in accounts:
                f.write("{}:{}\n".format(i, accounts[i]))
        with open("proxies.txt", "w") as f:
            f.write(proxy)
        os.system("touch access_tokens.txt authenticated_accounts.txt")
        if sys.platform.find("win32") == -1:
            os.system("./authenticator > /dev/null 2>&1")
        else:
            os.system("authenticator.exe > NUL 2>&1")
        with open("access_tokens.txt") as f:
            access_token = f.read().strip().splitlines()
        for i in range(len(access_token)):
            access_token[i] = access_token[i].strip()
            access_token[i] = "\"{}\"".format(access_token[i])
        with open("./access_tokens.json", "w") as f:
            f.write("[")
            f.write(",".join(access_token))
            f.write("]")
        with open("./authenticated_accounts.txt", "r") as f:
            authenticated_accounts = f.read().strip().splitlines()
        for i in authenticated_accounts:
            i = i.strip().split(":")[0]
            INFO("authenticated account: {}".format(i))
        os.system("rm access_tokens.txt authenticated_accounts.txt proxies.txt accounts.txt")


        # run
        cmd = "./freechatgpt"
        try:
            screenData = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=False)
            while True:
                line = screenData.stdout.readline().decode("utf-8").strip()
                if line.find("[GIN]") != -1:
                    status = line.split()[5].strip()
                    if status == "200":
                        INFO(line)
                    elif status[0] == "5":
                        ERROR(line)
                        ERROR("detected 5xx, restarting...")
                        screenData.terminate()
                        break
                    else:
                        WARNING(line)
                else:
                    INFO(line)
        except:
            screenData.terminate()
        