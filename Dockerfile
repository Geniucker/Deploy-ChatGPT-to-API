FROM golang:1.20.3-alpine as builder

COPY ChatGPT-to-API /root/ChatGPT-to-API

WORKDIR /root/ChatGPT-to-API


ENV http_proxy=socks5://host.docker.internal:7895
ENV https_proxy=socks5://host.docker.internal:7895
ENV ALL_PROXY=socks5://host.docker.internal:7895

RUN go build && \
    cd tools/authenticator && \
    go build && \
    chmod -R +x /root/ChatGPT-to-API


FROM python:3.9-slim
LABEL Name=chatgpttoapi Version=0.0.1

WORKDIR /app

COPY --from=builder /root/ChatGPT-to-API/freechatgpt /app/freechatgpt
COPY --from=builder /root/ChatGPT-to-API/tools/authenticator/authenticator /app/authenticator
COPY run.py /app/run.py

EXPOSE 8080

CMD ["python3", "run.py"]
