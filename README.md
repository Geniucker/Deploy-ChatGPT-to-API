# Deploy ChatGPT-to-API
[中文文档](./README_zh.md)  English Docs  
These days I found an interesting repo [ChatGPT-to-API](https://github.com/acheong08/ChatGPT-to-API). You can deploy a *fake* API using the web version of ChatGPT.  
However, it's docs are not specific. This repo is to help you easily config and deploy [ChatGPT-to-API](https://github.com/acheong08/ChatGPT-to-API).  

## Features
Original Project Features:  
- Implemented a local Fake API based on a web version of reverse engineering.  
- Supports calling all models supported by the web version (GPT-4 requires Plus subscription).  
- Supports multiple users to prevent triggering rate limits.  
- Implemented APIs:  
  - `/v1/chat/completions`  
  - `/v1/engines`: The original project accessed this api to obtain available models using the official API and key. However, since it relies on the web-based API, it is not very meaningful. Moreover, this API is temporarily unavailable in order to implement custom API keys.  
  -  `/v1/models`: The original project accessed this api to obtain available models using the official API and key. However, since it relies on the web-based API, it is not very meaningful. Moreover, this API is temporarily unavailable in order to implement custom API keys.  

Additional Features I have added:  
- Implemented automatic retrieval of access_token using emails and passwords, and automatically refreshes the access_token upon expiration (only applicable for email password login; Google and Microsoft logins require manual access_token input). The original project only supports single-account one-click login, while this project supports multiple-account one-click access_token retrieval.  
- Implemented authentication. The original project, being based on reverse engineering of the web version, does not require API key verification. However, for added security, I have added a validation feature where you can set the desired API key for request verification. If not needed, you can leave it blank.  
- Supports https. You should only provide certificates and keys and there's no need to use nginx or other reverse proxy.  

## Requirements
- git  
- python3  
- Docker (if deploy in Docker)  
- golang and `go` command in PATH (if deploy in host)  
- One or more ChatGPT accounts  

## Steps
1. Clone this repo to somewhere (suppose `/dcta/`)  
2. Edit the following variables in `run.py`:  
   - `proxy`: format: `host:port`. If you don't need proxy, set it to `""`  
   - `proxy_type`: possible values: `"socks5"` or `"http"`  
   - `accounts`: It's a dictionary of accounts' info. Multiple users are supported. See the example bellow  
   - `server_host`: the host you want ChatGPT-to-API to listen  
   - `server_port`: the port you want ChatGPT-to-API to listen  
   - `custom_API_key`: In theory, since the original project is based on reverse engineering of the web version, there is no need to verify the API key. However, for security purposes, I have added an authentication feature where you can set the desired API key to validate the requests. If you don't need it, you can leave it blank.  
   - `cert_filename`: the filename of the certificate file. Not the path. If you don't need https, set it to `""`  
   - `key_filename`: the filename of the key file. Not the path. If you don't need https, set it to `""`  

![image](https://github.com/Geniucker/Deploy-ChatGPT-to-API/assets/61449208/5c33d3f9-bf21-4a04-af34-579dc6e5fe73)  
3. **If deployed in host**: run `pip3 install -r requirements.txt`  
   **If deployed in docker**: nothing to do in this step  
4. run `build.py` and follow the instructions (You may need to use `sudo` to get the permission of Docker).  
5. run the service:  
   **If deployed in docker**:  
   open a terminal in `/dcta/`. run `docker compose up -d`  
   **If deployed in host**:
   open a terminal in `/dcta/`. run `run.py`  
6. setup https (optional):  
   **If deployed in docker**:  
   modify the `volumes` field in `docker-compose.yml` to replace `./certifications` with the path of your certifications. As the screenshot bellow:  
   ![image](https://github.com/Geniucker/Deploy-ChatGPT-to-API/assets/61449208/2ae9c330-c360-40f1-b741-03c217191e11)  
   **If deployed in host**:  
   Place the certificate and key in or create a symbolic link to the `certifications` folder.  
7. Enjoy~

## FAQ
- Q: What if the access_token of OpenAI expire?  
  A: If this happen, the request to the fake api will cause `401` status code in ChatGPT-to-API. I use python to inspect this code and will regenerate access_token and restart ChatGPT-to-API automatically.  
- Q: Why do I get a 404 error?  
  A: Please refer to the "Implemented APIs" section in the [Features](#Features) section. Accessing a non-existent interface will return a 404 error. Additionally, the `/v1/chat/completions` interface does not support GET requests, so accessing it directly from a browser will also result in a 404 error.  
- Q: Why do I get a 500 error?  
  A: A 500 error is typically related to IP issues, meaning that your IP address has been banned by OpenAI.  
- Q: Where can I find logs  
  A: This project is divided into two parts. One part is the auxiliary for ChatGPT-to-API, which handles operations like token retrieval and automatic token refresh. Its logs are directly printed on the console.  
  The other part is implemented in Go for authentication and HTTPS. Its logs are located in the `log` folder, specifically in the `authentication.log` file.  
  For deployments within Docker, you can view the container logs to see the logs of the former part. As for the logs of the latter part, you can find them in `log/authentication.log` on the host machine.  

## Contribution
Welcome to raise issues and PRs.  
For bugs, please refer to the log viewing method in the FAQ and provide the logs.  
![log](https://github.com/Geniucker/Deploy-ChatGPT-to-API/assets/61449208/e8472434-780d-4dcc-aaa1-75154c21b917)  
