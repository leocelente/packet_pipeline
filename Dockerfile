FROM python:3.10-alpine
WORKDIR /
RUN apk update && apk add git make gcc libc-dev
RUN git clone https://github.com/rs1729/RS.git /decoder && cd /decoder/demod/mod && make rs41mod
RUN git clone https://github.com/leocelente/packet_pipeline.git /app
WORKDIR /app
RUN python3.10 -m pip install -r requirements.txt
ENTRYPOINT [ "python3.10", "/app/main.py" ]
