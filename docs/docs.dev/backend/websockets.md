# Websockets
Sometimes we want to communicate with the front-end without that the frontend has send anything to the backend (for example live updating of incoming chat messages).
To do this we use websockets. To make sure we can form 'pools' of people that would receive anything on a change (like an extra chat message in an alliance), we use
connection pools. When a user opens a websocket it will be assigned to a 'connection pool' based on an attribute like, alliance name, etc. Using these pools we can easily communicate to all users in this pool.
