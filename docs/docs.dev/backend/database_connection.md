# Database connection

## Overview
How we establish sessions for our database

## Technologies used
- sqlalchemy (async)

## Description
The configuration for connecting to the database is done using confz.

Upon staring up our API we establish a connection to the database.
We create a async_sessionmaker which will generate async sessions for us to use inside the api.

If the API shuts down our connection to the database is gracefully closed. 'database.py' handles this connection
## To Verify
Make sure the configuration is correct with the database you want to connect with.
Make sure the database is ready to accept connections.

## Additional Information

Here is an example python function on how to use the async session.
```python
@app.get("/me")
async def me(user_id: Annotated[UUID, Depends(get_my_id)], db=Depends(db.get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().all()
```
