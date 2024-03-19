# OAuth2 with Password (and hashing), Bearer with JWT tokens

## Overview
This is how users can sign-up or sign-in to the game.

## Technologies used
- fastapi
- sqlalchemy
- postgresql
- pyton-jose
- HS256
- oath2
- passlib

## Description

### Auth router
We created a seperate fastapi router for authentication.
This router has 2 endpoints:
- `/add_user` - register a user
- `/token` - login a user by getting a JWT token in return

### Password hashing
The requested password will be hashed. This is to ensure incase the database gets stolen, the users's passwords won't be in plaintext. The library we used to hash passwords is `passlib`. And the algorithm we used is `Bcrypt`. 

By creating a password context, hashing and matching passwords can be done easily.
```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# verify
pwd_context.verify(plain_password, hashed_password)
# hash
pwd_context.hash(password)
```

### JWT

Our JWT tokens are generated with the python library `python-jose`. The algorithm used to sign the JWT is `HS256`. We also generated a secret key for generating the token. And an expiration time is also specified. Now if a user logs in succesfully they get a token in response.

With this token we can retrieve the user id for all the user specific requests.

### Adding users

For adding a user, sqlalchemy will try to insert a user to the table. If this fails the email or username are already be inside the database.

## Issues
- database: make sure the User table is present in the database

## Additional Information

- make sure you read this section about JWT: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#about-jwt 