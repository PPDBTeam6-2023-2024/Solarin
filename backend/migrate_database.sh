alembic revision --autogenerate -m ""
alembic upgrade head
python3 fill_db.py