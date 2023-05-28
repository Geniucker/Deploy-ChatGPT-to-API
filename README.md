# Deploy ChatGPT to API
These days I found an interesting repo [ChatGPT to API](https://github.com/acheong08/ChatGPT-to-API). You can deploy a *fake* API using the web version of ChatGPT.  
However, it's docs are not specific. This repo is to help you easily config and deploy [ChatGPT to API](https://github.com/acheong08/ChatGPT-to-API).  

## Requirements
- git  
- Docker (if deploy in Docker)  
- golang and `go` command in PATH (if deploy in host)  
- One or more ChatGPT accounts  

## Steps
1. Clone this repo to somewhere (suppose `/dcta/`)  
2. Edit the following variables:  
   - `proxy`: format: `host:port`. If you don't need proxy, set it to `""`  
   - `proxy_type`: possible values: `"socks5"` or `"http"`  
   - `accounts`: It's a dictionary of accounts' info. Multiple users are supported. See the example bellow  
   - `server_host`: the host you want ChatGPT-to-API to listen  
   - `server_port`: the port you want ChatGPT-to-API to listen  

![image](https://github.com/Geniucker/Deploy-ChatGPT-to-API/assets/61449208/73dc990a-a1f2-4c29-99bd-fbfba1077ee1)  
3. run `build.py` and follow the instructions.  
4. run the service:  
   **If deployed in docker**:  
   open a terminal in `/dcta/`. run `docker compose up -d --build`  
   **If deployed in host**:
   open a terminal in `/dcta/`. run `run.py`  
5. Enjoy~

## FAQ
- Q: What if the access_token of OpenAI expire?  
  A: If this happen, the request to the fake api will cause `500` status code in ChatGPT-to-API. I use python to inspect this code and will regenerate access_token and restart ChatGPT-to-API automatically.  
