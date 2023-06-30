# 部署 ChatGPT-to-API
中文文档  [English Docs](./README.md)  
最近发现了一个有趣的项目 [ChatGPT-to-API](https://github.com/acheong08/ChatGPT-to-API)，可以将 ChatGPT 的网页版部署为一个 API。  
但是它的文档不够详细，这个项目就是为了帮助你更方便地配置和部署 [ChatGPT-to-API](https://github.com/acheong08/ChatGPT-to-API)。  

## 特性
原项目功能：  
- 基于网页版的逆向工程实现了一个本地的 Fake API  
- 支持调用网页版支持的所有模型（当然 GPT-4 需要你是 Plus）  
- 支持多用户，从而防止触发频率限制  

我增加的功能：  
- 实现了账号密码自动获取 access_token，并在到期后自动刷新新的 access_token（仅限账号密码登录，谷歌和微软登录只能手动填写 access_token，同时原项目只支持单账号一键登录，本项目支持了多账户一键获取 access_token）  
- 实现了鉴权。原项目是基于对网页版的逆向工程，所以不需要验证 API key。但是，为了安全起见，我添加了一个验证功能，你可以设置想要的 API key 来验证请求。如果不需要，可以留空。  


## 依赖
- git  
- python3  
- Docker (如果在 Docker 中部署)  
- golang 和 `go` 命令在 PATH 中 (如果在主机中部署)  
- 至少一个 ChatGPT 账号  

## 步骤
1. 将这个仓库克隆到某个地方 (假设为 `/dcta/`)  
2. 编辑 `run.py` 中的以下变量:  
   - `proxy`: 格式: `host:port`。如果不需要代理，设置为 `""`  
   - `proxy_type`: 可能的值: `"socks5"` 或 `"http"`  
   - `accounts`: 它是一个账号信息的字典。支持多个用户。参考下面的例子  
   - `server_host`: 你想让 ChatGPT-to-API 监听的主机  
   - `server_port`: 你想让 ChatGPT-to-API 监听的端口  
   - `custom_API_key`: 理论上，由于原项目是基于对网页版的逆向工程，所以不需要验证 API key。但是，为了安全起见，我添加了一个验证功能，你可以设置想要的 API key 来验证请求。如果不需要，可以留空。  

![image](https://github.com/Geniucker/Deploy-ChatGPT-to-API/assets/61449208/7fc9afe8-374e-4d58-908d-b3a561ada9cd)  
3. **如果在主机中部署**: 运行 `pip3 install -r requirements.txt`  
   **如果在 Docker 中部署**: 这一步不需要做任何事情  
4. 运行 `build.py` 并按照提示操作。  
5. 运行服务:  
   **如果在 Docker 中部署**:  
   在 `/dcta/` 中打开一个终端。运行 `docker compose up -d`  
   **如果在主机中部署**:  
   在 `/dcta/` 中打开一个终端。运行 `run.py`  
6. 尽情享用吧~  

## FAQ
- Q: 如果 OpenAI 的 access_token 过期了怎么办？  
  A: 如果发生这种情况，对 fake api 的请求将在 ChatGPT-to-API 中导致 `401` 状态码。我使用 python 检查这个代码，并将自动生成 access_token 并自动重启 ChatGPT-to-API。  