FROM python:3.10-slim-buster

RUN apt update && apt install -y nginx

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


RUN rm /etc/nginx/sites-available/default
COPY scripts/nginx/default.conf /etc/nginx/sites-available/default


COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

RUN mkdir -p /app/media/

VOLUME ["/app/media/"]
VOLUME ["/app/api/django_static/"]

COPY . .

EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]

CMD ["bash", "-c", "gunicorn --workers 2 --preload --timeout=600 --bind 0.0.0.0:8000 api.conf.wsgi & nginx -g 'daemon off;'"]
