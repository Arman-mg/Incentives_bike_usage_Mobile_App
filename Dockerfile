FROM python:3.10-slim

ENV PYTHONUNBUFFERD True 


ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirement.txt 

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

