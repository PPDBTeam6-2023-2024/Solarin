#!/bin/bash
source env/bin/activate
cd src/ProgDBTutor
gunicorn --bind 0.0.0.0:5000 wsgi:app
sudo systemctl enable webapp
sudo systemctl start webapp
sudo systemctl restart nginx
echo output!!!!!!!!

/bin/bash
