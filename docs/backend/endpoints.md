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

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>Chat: '/chat'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>Logic: '/logic'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>CityManagement: '/cityManager'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>Planets: '/planet'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>Armies: '/army'</strong></summary>
<p>
This router will handle the communication about Armies and their actions

|  Endpoint   | Method | Purpose                                                 |
|:-----------:|:------:|:--------------------------------------------------------|
|   armies    |  GET   | Get all the armies on a specific planet                 |
|   troops    |  GET   | Get all troops and stats of an army                     |
| armies_user |  GET   | Get all the armies that are owned by the accessing user |

</p>
</details>

<details>
<summary><strong>BuildingManagement: '/building'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>UnitManagement: '/unit'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>

<details>
<summary><strong>Spawn: '/spawn'</strong></summary>
<p>

| Endpoint | Method | Purpose                                                                                                                                                  |
|:--------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|   User   |  Data  | Store data of a user their account                                                                                                                       |

</p>
</details>
