#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput, Popen, PIPE, STDOUT
import os
import base64
import hashlib
import requests
from urllib.parse import urlparse, parse_qs
from certifi import where

proxy = "localhost:7890"  # if you don't use proxy, set it to ""
proxy_type = "socks5"  # socks5 or http
accounts = {
    "user1": "password1",
    # "user2": "password2"
}
access_tokens = [
    # "your access token",
    # "your another access token"
]
server_host = "0.0.0.0"
server_port = "8080"  # if deploy in docker, set it to "8080"


def ERROR(msg):
    print("\033[31m[ERROR]\033[0m" + msg)
def INFO(msg):
    print("\033[32m[INFO]\033[0m" + msg)
def WARNING(msg):
    print("\033[33m[WARNING]\033[0m" + msg)
def generate_code_verifier():
    # 随机生成一个长度为 32 的 code_verifier
    token = os.urandom(32)
    code_verifier = base64.urlsafe_b64encode(token).rstrip(b'=')
    return code_verifier.decode('utf-8')
def generate_code_challenge(code_verifier):
    # 对 code_verifier 进行哈希处理，然后再进行 base64url 编码，生成 code_challenge
    m = hashlib.sha256()
    m.update(code_verifier.encode('utf-8'))
    code_challenge = base64.urlsafe_b64encode(m.digest()).rstrip(b'=')
    return code_challenge.decode('utf-8')
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
class Auth0:
    def __init__(self, email: str = None, password: str = None, access_token: str = None, proxy: str = None, code_verifier: str = None, code_challenge: str = None):
        self.session_token = None
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.code_verifier = code_verifier
        self.code_challenge = code_challenge
        self.req_kwargs = {
            'proxies': {
                'http': proxy,
                'https': proxy,
            } if proxy else None,
            'verify': where(),
            'timeout': 100,
        }
        self.access_token = access_token
        self.refresh_token = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/109.0.0.0 Safari/537.36'
    def __del__(self):
        if self.refresh_token:
            url = "https://auth0.openai.com/oauth/revoke"
            headers = {
                'User-Agent': self.user_agent
            }
            data = {
                "client_id": "pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh",
                "token": self.refresh_token
            }
            self.session.post(url, headers=headers, data=data, **self.req_kwargs)
    def refresh(self) -> str:
        if self.email is None or self.password is None and self.access_token is not None:
            return self.access_token
        elif self.refresh_token:
            url = "https://auth0.openai.com/oauth/token"
            headers = {
                'User-Agent': self.user_agent
            }
            data = {
                "redirect_uri": "com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback",
                "grant_type": "refresh_token",
                "client_id": "pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh",
                "refresh_token": self.refresh_token
            }
            resp = self.session.post(url, headers=headers, data=data, **self.req_kwargs)
            if resp.status_code == 200:
                json = resp.json()
                self.access_token = json['access_token']
                INFO('Refresh token of {} successfully.'.format(self.email))
                return self.access_token
            else:
                raise Exception('Error refresh token.')
        else:
            return self.auth()
    def auth(self) -> str:
        return self.__part_two()
    def __part_two(self) -> str:
        code_challenge = self.code_challenge
        code_verifier = self.code_verifier
        url = 'https://auth0.openai.com/authorize?client_id=pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh&audience=https%3A%2F' \
                '%2Fapi.openai.com%2Fv1&redirect_uri=com.openai.chat%3A%2F%2Fauth0.openai.com%2Fios%2Fcom.openai.chat' \
                '%2Fcallback&scope=openid%20email%20profile%20offline_access%20model.request%20model.read' \
                '%20organization.read%20offline&response_type=code&code_challenge={}' \
                '&code_challenge_method=S256&prompt=login'.format(code_challenge)
        return self.__part_three(code_verifier, url)
    def __part_three(self, code_verifier, url: str) -> str:
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://ios.chat.openai.com/',
        }
        resp = self.session.get(url, headers=headers, allow_redirects=True, **self.req_kwargs)
        if resp.status_code == 200:
            try:
                url_params = parse_qs(urlparse(resp.url).query)
                state = url_params['state'][0]
                return self.__part_four(code_verifier, state)
            except IndexError as exc:
                raise Exception('Rate limit hit.') from exc
        else:
            raise Exception('Error request login url.')
    def __part_four(self, code_verifier: str, state: str) -> str:
        url = 'https://auth0.openai.com/u/login/identifier?state=' + state
        headers = {
            'User-Agent': self.user_agent,
            'Referer': url,
            'Origin': 'https://auth0.openai.com',
        }
        data = {
            'state': state,
            'username': self.email,
            'js-available': 'true',
            'webauthn-available': 'true',
            'is-brave': 'false',
            'webauthn-platform-available': 'false',
            'action': 'default',
        }
        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            return self.__part_five(code_verifier, state)
        else:
            raise Exception('Error check email.')
    def __part_five(self, code_verifier: str, state: str) -> str:
        url = 'https://auth0.openai.com/u/login/password?state=' + state
        headers = {
            'User-Agent': self.user_agent,
            'Referer': url,
            'Origin': 'https://auth0.openai.com',
        }
        data = {
            'state': state,
            'username': self.email,
            'password': self.password,
            'action': 'default',
        }
        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            location = resp.headers['Location']
            if not location.startswith('/authorize/resume?'):
                raise Exception('Login failed.')
            return self.__part_six(code_verifier, location, url)
        if resp.status_code == 400:
            raise Exception('Wrong email or password.')
        else:
            raise Exception('Error login.')
    def __part_six(self, code_verifier: str, location: str, ref: str) -> str:
        url = 'https://auth0.openai.com' + location
        headers = {
            'User-Agent': self.user_agent,
            'Referer': ref,
        }
        resp = self.session.get(url, headers=headers, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            location = resp.headers['Location']
            if location.startswith('/u/mfa-otp-challenge?'):
                if not self.mfa:
                    raise Exception('MFA required.')
                return self.__part_seven(code_verifier, location)
            if not location.startswith('com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback?'):
                raise Exception('Login callback failed.')
            return self.get_access_token(code_verifier, resp.headers['Location'])
        raise Exception('Error login.')
    def __part_seven(self, code_verifier: str, location: str) -> str:
        url = 'https://auth0.openai.com' + location
        data = {
            'state': parse_qs(urlparse(url).query)['state'][0],
            'code': self.mfa,
            'action': 'default',
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': url,
            'Origin': 'https://auth0.openai.com',
        }

        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            location = resp.headers['Location']
            if not location.startswith('/authorize/resume?'):
                raise Exception('MFA failed.')

            return self.__part_six(code_verifier, location, url)

        if resp.status_code == 400:
            raise Exception('Wrong MFA code.')
        else:
            raise Exception('Error login.')
        
    def get_access_token(self, code_verifier: str, callback_url: str) -> str:
        url_params = parse_qs(urlparse(callback_url).query)

        if 'error' in url_params:
            error = url_params['error'][0]
            error_description = url_params['error_description'][0] if 'error_description' in url_params else ''
            raise Exception('{}: {}'.format(error, error_description))

        if 'code' not in url_params:
            raise Exception('Error get code from callback url.')

        url = 'https://auth0.openai.com/oauth/token'
        headers = {
            'User-Agent': self.user_agent,
        }
        data = {
            'redirect_uri': 'com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback',
            'grant_type': 'authorization_code',
            'client_id': 'pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh',
            'code': url_params['code'][0],
            'code_verifier': code_verifier,
        }
        resp = self.session.post(url, headers=headers, json=data, allow_redirects=False, **self.req_kwargs)

        if resp.status_code == 200:
            json = resp.json()
            if 'access_token' not in json:
                raise Exception('Get access token failed, maybe you need a proxy.')
            self.access_token = json['access_token']
            self.refresh_token = json['refresh_token']
            INFO('Get access token of {} successfully.'.format(self.email))
            return self.access_token
        else:
            raise Exception(resp.text)


if __name__=="__main__":
    if proxy.split(":")[0] in ["127.0.0.1", "localhost", "::1"] and os.path.exists("/.dockerenv"):
        proxy = "host.docker.internal:{}".format(proxy.split(":")[1])
    if proxy != "":
        proxy = "{}://{}".format(proxy_type, proxy)
    else: proxy = None
    os.environ["SERVER_HOST"] = server_host
    os.environ["SERVER_PORT"] = server_port
    os.environ["GIN_MODE"] = "release"
    accout_objs = []
    for i in accounts:
        accout_objs.append(
            Auth0(
                email=i,
                password=accounts[i],
                proxy=proxy,
                code_challenge=code_challenge,
                code_verifier=code_verifier
            )
        )
    for i in access_tokens:
        accout_objs.append(
            Auth0(
                access_token=i,
                proxy=proxy,
                code_challenge=code_challenge,
                code_verifier=code_verifier
            )
        )
    while True:
        # config access_tokens
        access_token = []
        for i in accout_objs:
            access_token.append(i.refresh())
        for i in range(len(access_token)):
            access_token[i] = access_token[i].strip()
            access_token[i] = "\"{}\"".format(access_token[i])
        with open("./access_tokens.json", "w") as f:
            f.write("[")
            f.write(",".join(access_token))
            f.write("]")


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
            exit()
        