FROM python:3.11

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt #для кэширования при создании image

COPY . .
RUN chmod a+x docker/*.sh #даем доступ к использованию всех .sh файлов
#WORKDIR src
#
#CMD gunicorn main:myapp --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

