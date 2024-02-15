# pull official base image
FROM python:3.11.2-slim-buster

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . .
RUN chmod +x deployment.sh
CMD /deployment.sh
