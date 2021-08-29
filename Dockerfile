FROM python:3.9.5-slim

LABEL app="wildoverflow"

ADD . ./app

RUN pip install -r ./app/requirements.txt

CMD [ "python", "./app/bot.py" ]
