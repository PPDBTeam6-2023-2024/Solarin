# Planet socket

## Overview
- The backend implementation of the planet websocket

## Technologies used
- websockets
- asyncio
- fastapi
- pytest

## Description
- This WebSocket endpoint (`/ws/{planet_id}`) is responsible for handling WebSocket connections related to a specific planet. It allows clients to subscribe to updates and perform actions such as retrieving armies on the planet and changing army directions in real-time.
- Upon connection, the client must provide a valid authentication token in the `Sec-WebSocket-Protocol` header to authenticate the user.
- The WebSocket handler interacts with the `DataAccess` layer to retrieve and update data related to armies on the planet.
- To execute an action you need to send a json to the websocket
  - `type`: the type of the action
  - Supported action types:
    - `get_armies`: Retrieves all armies currently on the planet and sends the data to the client.
      - Response: 
        - `request_type`: type of the request, this will be `get_armies`
        - `data`: the response data which is an array of **armies**
    - `change_direction`: Changes the direction of a specific army on the planet based on client input and broadcasts the updated army data to all connected clients.
      - extra json parameters:
        - `army id`: id of army
        - `to_x`: x coordinate to move to
        - `to_y`: y coordinate to move to
        - `on_arrive` (optional): Indicates whether or not to do some special onArrive action when our army arrives
          - `target_id`: id of the target to do the event with
          - `target_type`: type of on Arrive event we will do
      - Response: 
        - `request_type`: type of the request, this will be `change_direction`
        - `data`: the updated **army**
- The connection is managed by the `ConnectionPool` class from `manager.py`, which ensures efficient handling of multiple clients and broadcasting updates to all connected clients.
- Upon disconnection (`WebSocketDisconnect`), the connection is properly closed and removed from the connection pool.
- Army response json: 
  - `id`: army id
  - `departure_time`: time the army left (last direction change received) in _isoformat_
  - `arrival_time`: time the army arrives at destination in _isoformat_
  - `x`: the from x position 
  - `y`: the from y position
  - `to_x`: the to x position 
  - `to_y`: the to y position

Relevant data calculation for retrieving the current position:
```python
current_time = datetime.utcnow()

total_time_diff = (army.arrival_time - army.departure_time).total_seconds()
current_time_diff = (min(current_time, army.arrival_time) - army.departure_time).total_seconds()

x_diff = army.to_x - army.x
y_diff = army.to_y - army.y

current_x = x_diff * (current_time_diff / total_time_diff)
current_y = y_diff * (current_time_diff / total_time_diff)
```


## Additional Information
- All the backend features are tested with pytest
- The handling of these events occurs in 'planet_socket_actions.py'
