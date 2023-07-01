# Deploy ChatGPT-to-API
[中文文档](./README_zh.md)  English Docs  
These days I found an interesting repo [ChatGPT-to-API](https://github.com/acheong08/ChatGPT-to-API). You can deploy a *fake* API using the web version of ChatGPT.  
However, it's docs are not specific. This repo is to help you easily config and deploy [ChatGPT-to-API](https://github.com/acheong08/ChatGPT-to-API).  

## Features

Original Project Features:  
- Implemented a local Fake API based on a web version of reverse engineering.  
- Supports calling all models supported by the web version (GPT-4 requires Plus subscription).  
- Supports multiple users to prevent triggering rate limits.  

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
4. run `build.py` and follow the instructions.  
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
