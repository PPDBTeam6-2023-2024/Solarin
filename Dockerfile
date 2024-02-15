# pull official base image
FROM python:3.11.2-slim-buster

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . .
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:app"]
CMD ["sudo", "systemctl", "restart", "webapp"]
