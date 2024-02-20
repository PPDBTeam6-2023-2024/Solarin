# Python backend setup

## Poetry
--- 
Poetry is a virtual environment like venv with just some more fancy configuration options. To install poetry just simply run > `pip install poetry`.
These are some handy poetry commands:

- poetry shell _(start virtual env shell)_
- poetry add <module> _(equivalent of pip install, you add this dependency)_
- poetry update _(update/install all the dependencies)_

All the other dependencies are already added to the poetry. So you only need to install poetry.

## FastAPI
---
This is our framework for the REST API for our game.
### Docs / Run
To start our app, simply run `python -m src.app`. Make sure the database you are connecting to (which chosen in config, see later) is ready.
Then you will see in the terminal that the application has started. You can access the automatically generated documentation at: `http://localhost:8000/docs`.
This is what you call the api-swagger. To log in a user click the lock button on the top right en enter the credentials of the user which is inside the database.
Then you will be able to try out the endpoint /me. Which will show you!

### Authorization
Authorization I did very close to the FastAPI documentation -> https://fastapi.tiangolo.com/tutorial/security/
The idea is simple, we have a passlib which can encrypt, decrypt passwords based on an encryption key.
This is important for privacy reasons. The endpoint /token will generate a token for a certain user, which is now valid for 30 minutes.
This token can now be used to call personal endpoints, which for example could be /get_army.
To make it a bit cleaner instead of putting all the code in the app file I created a separate authorization router.

### CORS
Because of our front-end backend setup we need CORS. Explanation here: https://fastapi.tiangolo.com/tutorial/cors/

## Sqlalchemy
---
With sqlalchemy a class was made, so we can set up an async connection with the database.
A simple user table was created.
And some simple queries on the user table are also created.

## Alembic
---
Alembic is a utility library for managing database schemes. With alembic we can create/update our database scheme starting from our sqlalchemy tables.
This makes database design very easy and flexible. 
If someone edits something in the sqlalchemy classes, then that person could add a revision and all the other uses can just update their current database without having to delete it fully.

Setup is done like followed:
In migrations you have a file .env
In that file you can import all the Base's so alembic knows all the tables.
A bit below that you can set up which database alembic needs to connect with.

These are some handy commands:
- alembic revision --autogenerate -m "<change>" _(this adds a revision to the database tables, its almost like commiting a change)_
- alembic upgrade head _(this updates/setups the database with the most recent scheme)_

## Confz
---
Confz is a simple library for configuration. https://github.com/Zuehlke/ConfZ

## Loguru
---
Loguru is a simple library for logging. https://github.com/Delgan/loguru
I also overrided the fastapi logger so that it uses Loguru.

