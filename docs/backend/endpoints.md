# Endpoints

## Overview
Explanation of what each endpoint does

## Technologies used
- FastApi

## Endpoints
Communication from frontend with the backend is done using the REST structure.
We use an authentication token to identify the user who is communicating with the backend

Our Endpoints are structured into multiple routers:

<details>
<summary><strong>Authentication: '/auth'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                          |
|:--------:|:------:|:-----------------------------------------------------------------|
| add_user |  POST  | Create a new user account                                        |
|  token   |  POST  | Let the user log in and receive an authentication token as reply |
| validate |  GET   | Check if a provided token is valid                               |
|    me    |  GET   | Get basic information about the user account                     |
</p>
</details>

<details>
<summary><strong>Chat: '/chat'</strong></summary>
<p>

|       Endpoint        |  Method   | Purpose                                                                              |
|:---------------------:|:---------:|:-------------------------------------------------------------------------------------|
|          dm           | WEBSOCKET | A websocket for a specific dm board (handles chat communication between users)       |
|      dm_overview      |    GET    | Get an overview of all the friends of a user (and provide their dm message board id) |
|    friend_requests    |    GET    | Get the friend requests send to the user                                             |
|    friend_requests    |   POST    | Send a friend request to another user or accept/reject a friend request              |
|    create_alliance    |   POST    | Create a new alliance                                                                |
|     join_alliance     |   POST    | Send a request to the alliance to ask to join them                                   |
|   alliance_requests   |    GET    | Get the requests from users to ask the alliance                                      |
|   alliance_requests   |   POST    | Accept/Reject an alliance request                                                    |
| alliance_messageboard |    GET    | Get the message board corresponding to the user his alliance                         |
|        ranking        |    GET    | Get the player ranking (based on amount of Solarium a user has)                      |


</p>
</details>

<details>
<summary><strong>Logic: '/logic'</strong></summary>
<p>
general logic information needed

|    Endpoint     | Method | Purpose                                             |
|:---------------:|:------:|:----------------------------------------------------|
|    resources    |  GET   | Get the current resources of a specific user        |
|    politics     |  GET   | Get the current political stance of a specific user |
| update_politics |  POST  | update the political stance of a user               |

</p>
</details>

<details>
<summary><strong>CityManagement: '/cityManager'</strong></summary>
<p>

|      Endpoint       | Method | Purpose                                                                                                                     |
|:-------------------:|:------:|:----------------------------------------------------------------------------------------------------------------------------|
|    get_city_data    |  GET   | Get the city information (rank, upgrade time remaining, region,..) and information of the buildings inside the city         |
|       cities        |  GET   | Get all cities on a specific planet                                                                                         |
| new_building_types  |  GET   | Retrieve types of buildings that we can build (We cannot build a type double)                                               |
|  get_upgrade_cost   |  GET   | Get the upgrade costs of the buildings inside a city                                                                        |
|     cities_user     |  GET   | Get all the cities owned by a specific user                                                                                 |
|    upgrade_city     |  POST  | upgrade the rank of a city by 1 and adjust user resources accordingly                                                       |
| get_resource_stocks |  GET   | Get the amount of resources currently in storage and the max capacity of each production building in the city               |


</p>
</details>

<details>
<summary><strong>Planets: '/planet'</strong></summary>
<p>

| Endpoint |  Method   | Purpose                                                                      |
|:--------:|:---------:|:-----------------------------------------------------------------------------|
| planets  |    GET    | Get all existing planets                                                     |
|    ws    | WEBSOCKET | Websocket to handle (potential) real time planet events (like army movement) |
| regions  |    GET    | Retrieve all regions that are a part of a planet                             |

</p>
</details>

<details>
<summary><strong>Armies: '/army'</strong></summary>
<p>
This router will handle the communication about Armies and their actions

|   Endpoint   | Method | Purpose                                                 |
|:------------:|:------:|:--------------------------------------------------------|
|    armies    |  GET   | Get all the armies on a specific planet                 |
|    troops    |  GET   | Get all troops and stats of an army                     |
| armies_user  |  GET   | Get all the armies that are owned by the accessing user |
| army_in_city |  GET   | Retrieve the army that is inside the city               |
| fleets_in_space |  GET   | Retrieve the fleets that are in space               |
| fleets  |  GET   | Retrieve the fleets of a user on a specific planet               |

</p>
</details>

<details>
<summary><strong>BuildingManagement: '/building'</strong></summary>
<p>

|      Endpoint       | Method | Purpose                                                      |
|:-------------------:|:------:|:-------------------------------------------------------------|
|   training_queue    |  GET   | Retrieve training queue information about a barrack building |                                                                                                                     |
| create_new_building |  POST  | Create a new building                                        |
|       collect       |  POST  | Collect resources from a specific building                   |
|  upgrade_building   |  POST  | Upgrade a specific building                                  |

</p>
</details>

<details>
<summary><strong>UnitManagement: '/unit'</strong></summary>
<p>

|  Endpoint  | Method | Purpose                                                            |
|:----------:|:------:|:-------------------------------------------------------------------|
| train_cost |  GET   | Get the training cost of a specific unit type                      |
|   train    |  POST  | Add a training queue entry to the training queue list of a barrack |

</p>
</details>

<details>
<summary><strong>Spawn: '/spawn'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                    |
|:--------:|:------:|:---------------------------------------------------------------------------|
|          |  GET   | Give information, on what the user needs to see when he/she opens the game |

</p>
</details>


<details>
<summary><strong>Spawn: '/trading'</strong></summary>
<p>

| Endpoint |  Method   | Purpose                         |
|:--------:|:---------:|:--------------------------------|
|    WS    | WEBSOCKET | Websocket for handeling trading |

</p>
</details>

<details>
<summary><strong>GeneralRouter: '/general'</strong></summary>
<p>

|      Endpoint      | Method | Purpose                                                             |
|:------------------:|:------:|:--------------------------------------------------------------------|
| available_generals |  GET   | Retrieve the generals that are still able to be assigned to an army |
|    add_general     |  POST  | Assign a general to an army                                         |
|   remove_general   |  POST  | Un-assign a general from an army                                    |

</p>
</details>