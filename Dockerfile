FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN python3.10 -m pip install -r requirements.txt
ENTRYPOINT [ "python3.10", "main.py" ]