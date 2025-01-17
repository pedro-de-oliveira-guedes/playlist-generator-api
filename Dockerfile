FROM python:3.11-slim-bullseye

WORKDIR /app

COPY app.py /app
COPY requirements.txt /app
COPY static /app/static
COPY templates /app/templates

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "app.py"]

EXPOSE 52055
