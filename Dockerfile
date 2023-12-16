FROM python:3.8-alpine
WORKDIR /
RUN apk update && apk add git make gcc libc-dev
RUN git clone https://github.com/rs1729/RS.git /decoder && cd /decoder/demod/mod && make rs41mod
# RUN git clone https://github.com/leocelente/packet_pipeline.git /app
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT [ "python3", "/app/main.py" ]
