FROM python:3.10.5-slim

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
COPY ./pytest.ini ./pytest.ini
COPY ./env/.env ./.env
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /app
