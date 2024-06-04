
# Spawn router

## Overview
The `/spawn` endpoint is responsible for spawning a user in a planet. It returns a JSON object with the key `planet_id` and the value as an integer representing the planet ID.

## Technologies used
- pytest
- fastapi

## Description
The `/spawn` endpoint performs the following actions:

1. If the user has any planets with a city on it, it returns the most recently visited planet.
2. If the user does not have any cities on planets, it queries the database for the planet that was most recently created within the past hour.
3. If no planet fits the above descriptions, it generates a random planet and returns the ID of the newly generated planet.

I the system detects that the user is starting as a new player. That player will receive the starting amount for each resource type.

## Issues
- Currently there must be a space region with id 1 present in the database in order for no errors to occur
- Tables in the database need to be up to date

## Additional Information
- Endpoints and database queries are tested using pytest
