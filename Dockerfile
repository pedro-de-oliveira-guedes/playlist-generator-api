FROM python:3.11-slim-bullseye

WORKDIR /app

COPY main.py /app/playlist-generator-api
COPY requirements.txt /app/playlist-generator-api

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
