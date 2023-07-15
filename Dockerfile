FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x asgi-entrypoint.sh

ENTRYPOINT [ "./asgi-entrypoint.sh" ]
