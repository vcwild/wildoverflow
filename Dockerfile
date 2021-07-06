FROM python:3.9.5

ADD . ./app

RUN pip install -r ./app/requirements.txt

CMD [ "python", "./app/bot.py" ]
