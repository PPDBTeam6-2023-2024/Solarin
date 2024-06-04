# Global Websocket Router

## Overview
This feature introduces a global websocket router `/globalws` with a `/ws` endpoint. It's primarily used for sending notifications to users.

## Technologies used
- Websockets

## Description
The global websocket router allows you to enqueue messages in a global queue. These messages must be dictionaries with a key 'target' which is the target user id. The rest of the dictionary will be sent to the correct websocket. Currently, this router is used for triggering a game over notification upon a player's death.

## Issues
Ensure that the messages enqueued in the global queue are dictionaries and contain a 'target' key. Without this, the message will not be sent.

## Additional Information
This router can be extended to support other types of notifications or messages in the future.

