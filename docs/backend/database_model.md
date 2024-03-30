# Database model

## Overview
Explanation of how our database model works and looks

## Technologies used
- sqlalchemy (async)

## Description
In our database model we can consider 2 types of Tables:

<details>
<summary><strong>Lookup Tables</strong></summary>
<p>
These type of tables can be filled by developers.
These tables are only supposed to be altered during development by the game and 
<br/> not because of the actions of a user. In our project we use such tables to add new types of troops, building, etc.
</p>
</details>
<details>
<summary><strong>Data Tables</strong></summary>
<p>
These tables can be used to store information about the game and can be altered by user interactions
</p>
</details>

An overview of each the tables in the database:

<details>
<summary><strong>User and Communication</strong></summary>
<p>

|      Table      | Type | Purpose                                                                                                                                                  |
|:---------------:|:----:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|      User       | Data | Store data of a users account                                                                                                                            |
|    Alliance     | Data | Store the alliances                                                                                                                                      |
|     Message     | Data | Store the messages                                                                                                                                       |
|  MessageBoard   | Data | Each message corresponds to a message board<br/> This table makes it possible to request sequences <br/>of messages from an alliance or between players. |
|    FriendsOf    | Data | Store which users are friends with each other                                                                                                            |
|  FriendRequest  | Data | Stores which users have pending friend requests                                                                                                          |
| AllianceRequest | Data | Stores which users have pending alliance requests to join an alliance (needs to be accepted by someone in the alliance)                                  |

</p>
</details>


<details>
<summary><strong>Planets and environment</strong></summary>
<p>

|      Table       |  Type  | Purpose                                                                     |
|:----------------:|:------:|:----------------------------------------------------------------------------|
|   SpaceRegion    |  Data  | Stores the regions in space                                                 |     
|      Planet      |  Data  | Stores the planets in the game                                              |     
|    PlanetType    | Lookup | Stores which types of planets are in the game <br/>(each planet has a type) |     
|   PlanetRegion   |  Data  | Stores the region corresponding to a planet                                 |     
| PlanetRegionType | Lookup | Store all the types a region can be                                         |     


</p>
</details>

<details>
<summary><strong>Settlements</strong></summary>
<p>

|           Table            |  Type   | Purpose                                                                                                                                                  |
|:--------------------------:|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|            City            |  Data   | Stores information about a city that is in a region on a planet                                                                                          |                                                                                                                                                  |     
|      BuildingInstance      |  Data   | Stores which buildings a city has                                                                                                                        |     
|        BuildingType        | Lookup  | Stores the types of buildings that can exist (This table is the parent of an ISA/polymorphic relation)                                                   |   
|        BarracksType        | Lookup  | Stores which types of barracks exist (This table is a child of an ISA/polymorphic relation with BuildingType)                                            |
|          WallType          | Lookup  | Stores which types of walls exist (This table is a child of an ISA/polymorphic relation with BuildingType)                                               |   
|         TowerType          | Lookup  | Stores which types of towers exist (This table is a child of an ISA/polymorphic relation with BuildingType)                                              |   
|         HouseType          | Lookup  | Stores which types of houses exist (This table is a child of an ISA/polymorphic relation with BuildingType)                                              |   
| ProductionBuildingTypeType | Lookup  | Stores which types of production buildings exist (This table is a child of an ISA/polymorphic relation with BuildingType)                                |   
|     ProducesResources      | Lookup  | Stores which resources a production building produces                                                                                                    |   
|        ResourceType        | Lookup  | Types of resources that are in the game                                                                                                                  |  
|        UpgradeCost         | Lookup  | Stores the cost to upgrade certain buildings                                                                                                             |


</p>
</details>

<details>
<summary><strong>Armies</strong></summary>
<p>

|     Table      |  Type  | Purpose                                                                                                                                          |
|:--------------:|:------:|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| TrainingQueue  |  Data  | One entry stores the training data of 1 Entry in a trainingQueue,<br/>The table keeps track of which units need to be trained and in which order |  
|   TroopType    | Lookup | Types of troops that are in the game                                                                                                             |
| TroopTypeCost  | Lookup | Stores which resources and how much of them it costs to train a unit                                                                             |
|      Army      |  Data  | Stores data about an army                                                                                                                        |
| ArmyConsistsOf |  Data  | The relation indication which types of units are part of the army and in what quantities                                                         |
|   TroopRank    |  Data  | Stores the rank of the unit for a specific user (if no entry, the rank is 1)                                                                     |

</p>
</details>

<details>
<summary><strong>Coordinate System</strong></summary>
<p>
The coordinate system used in our game is stored in the database as double precision (x,y) coordinate with values ranging from 0 to 1. Cities and planets have coordinates.
</p>
</details>

These models are created in SQL Alchemy and are generated using alembic

## Issues


## Additional Information
