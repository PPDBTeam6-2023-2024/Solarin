# Database model

## Overview
Explanation of how our database model works and looks

## Technologies used
- sqlalchemy (async)

## Tables
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

|       Table        |  Type  | Purpose                                                                                                                                                  |
|:------------------:|:------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
|        User        |  Data  | Store data of a user their account                                                                                                                       |
|      Alliance      |  Data  | Store the alliances                                                                                                                                      |
|      Message       |  Data  | Store the messages                                                                                                                                       |
|    MessageBoard    |  Data  | Each message corresponds to a message board<br/> This table makes it possible to request sequences <br/>of messages from an alliance or between players. |
|     FriendsOf      |  Data  | Store which users are friends with each other                                                                                                            |
|   FriendRequest    |  Data  | Stores which users have pending friend requests                                                                                                          |
|  AllianceRequest   |  Data  | Stores which users have pending alliance requests to join an alliance (needs to be accepted by someone in the alliance)                                  |
|  PoliticalStance   | LOOKUP | Stores all the political ideologies in our game                                                                                                          |
| HasPoliticalStance |  Data  | Stores information about the political direction of the user                                                                                             |

</p>
</details>


<details>
<summary><strong>Planets and environment</strong></summary>
<p>

|      Table       |  Type  | Purpose                                                                     |
|:----------------:|:------:|:----------------------------------------------------------------------------|
|      Planet      |  Data  | Stores the planets in the game                                              |     
|    PlanetType    | Lookup | Stores which types of planets are in the game <br/>(each planet has a type) |     
|   PlanetRegion   |  Data  | Stores the region corresponding to a planet                                 |     
| PlanetRegionType | Lookup | Store all the types a region can be                                         |     
|  AssociatedWith  | Lookup | Stores which region types can exist on which planet types                   |     


</p>
</details>

<details>
<summary><strong>Settlements</strong></summary>
<p>

|             Table             |  Type  | Purpose                                                                                                                   |
|:-----------------------------:|:------:|:--------------------------------------------------------------------------------------------------------------------------|
|             City              |  Data  | Stores information about a city that is in a region on a planet                                                           |                                                                                                                                                  |     
|       BuildingInstance        |  Data  | Stores which buildings a city has                                                                                         |     
|         BuildingType          | Lookup | Stores the types of buildings that can exist (This table is the parent of an ISA/polymorphic relation)                    |   
|     BuildingUpgradeQueue      | Lookup | Stores the buildings being upgraded                                                                                       |   
|         BarracksType          | Lookup | Stores which types of barracks exist (This table is a child of an ISA/polymorphic relation with BuildingType)             |
|           WallType            | Lookup | Stores which types of walls exist (This table is a child of an ISA/polymorphic relation with BuildingType)                |   
|           TowerType           | Lookup | Stores which types of towers exist (This table is a child of an ISA/polymorphic relation with BuildingType)               |   
|           HouseType           | Lookup | Stores which types of houses exist (This table is a child of an ISA/polymorphic relation with BuildingType)               |   
|    ProductionBuildingType     | Lookup | Stores which types of production buildings exist (This table is a child of an ISA/polymorphic relation with BuildingType) |   
|       ProducesResources       | Lookup | Stores which resources a production building produces                                                                     |   
|         CreationCost          | Lookup | Stores the cost to create/upgrade certain buildings                                                                       |
|           CityCosts           | Lookup | Stores the base cost to create/upgrade a city                                                                             |
|        CityUpdateQueue        | Lookup | Stores the cities being upgraded                                                                                          |


</p>
</details>

<details>
<summary><strong>Armies</strong></summary>
<p>

|      Table      |  Type  | Purpose                                                                                                                                                                                                                 |
|:---------------:|:------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  TrainingQueue  |  Data  | One entry stores the training data of 1 Entry in a trainingQueue,<br/>The table keeps track of which units need to be trained and in which order                                                                        |  
|    TroopType    | Lookup | Types of troops that are in the game                                                                                                                                                                                    |
|  TroopTypeCost  | Lookup | Stores which resources and how much of them it costs to train a unit                                                                                                                                                    |
|      Army       |  Data  | Stores data about an army                                                                                                                                                                                               |
| ArmyConsistsOf  |  Data  | The relation indication which types of units are part of the army and in what quantities                                                                                                                                |
|    TroopRank    |  Data  | Stores the rank of the unit for a specific user (if no entry, the rank is 1)                                                                                                                                            |
| AttackOnArrive  |  Data  | To handle actions when an army arrives in an IDLE manner we use this table to keep track of events that need to occur when an army arrives at its destination (This table is the parent of an ISA/polymorphic relation) |
|   AttackArmy    |  Data  | Stores which other army we might attack when our army arrives at its position  (This table is a child of an ISA/polymorphic relation with AttackArmy)                                                                   |
|   AttackCity    |  Data  | Stores which city we might attack when our army arrives at its position     (This table is a child of an ISA/polymorphic relation with AttackArmy)                                                                      |
|    EnterCity    |  Data  | Stores which city we might enter when our army arrives at its position     (This table is a child of an ISA/polymorphic relation with AttackArmy)                                                                       |
|   MergeArmies   |  Data  | Stores which army we merge with when we arrive     (This table is a child of an ISA/polymorphic relation with AttackArmy)                                                                                               |
|   ArmyInCity    |  Data  | Stores the armies that are present inside a city                                                                                                                                                                        |
|      Stat       | Lookup | Table for all types of stats of an army                                                                                                                                                                                 |
|  TroopHasStat   | Lookup | Association between stats and troop type                                                                                                                                                                                |
|    Generals     | Lookup | Stores all the general types                                                                                                                                                                                            |
| ArmyHasGeneral  |  Data  | Stores whether a general is assigned to a specific army                                                                                                                                                                 |
| GeneralModifier | Lookup | Stores which modifiers this general provide when the general is in the army                                                                                                                                             |
|   EnterPlanet   |  Data  | Stores which planet we might enter when our fleet arrives at its position (This table is a child of an ISA/polymorphic relation with OnArrive)                                                                          |

</p>
</details>

<details>
<summary><strong>Resources</strong></summary>
<p>

|          Table           |  Type  | Purpose                                                                                                           |
|:------------------------:|:------:|:------------------------------------------------------------------------------------------------------------------|
|       ResourceType       | Lookup | Types of resources that are in the game                                                                           |  
|       HasResources       |  Data  | Store resources associated with a user (stores how many of the resources a user has)                              |
|        TradeOffer        |  Data  | Stores the currently active trading offers                                                                        |
|        TradeGives        |  Data  | This table stores which resources a user will give to the trade offer setter when he/she accepts the trade offer. |
|      TradeReceives       |  Data  | This table stores which resources a user will receive from the trade offer setter when he/she accepts the trade   |
| ProductionRegionModifier |  Data  | Stores the modifiers applied to resource production based on the planet's region type.                            |
|     MaintenanceTroop     | Lookup | Stores The maintenance cost for a specific troop type                                                             |
|   MaintenanceBuilding    | Lookup | Stores The maintenance cost for a specific building type                                                          |


</p>
</details>

<details>
<summary><strong>Coordinate System</strong></summary>
<p>
The coordinate system used in our game is stored in the database as double precision (x,y) coordinate with values ranging from 0 to 1. 
Cities, Armies and regions have coordinates to keep track of their location.
</p>
</details>




<details>
<summary><strong>Domains</strong></summary>
<p>
The following domains are used:

|     Domain      | Purpose                                      |
|:---------------:|:---------------------------------------------|
|   Coordinate    | Domain for coordinates                       |  
| PositiveInteger | Domain for integers that need to be positive |  
|   Percentage    | Value in range between [-1, 1]               |  
|     Decimal     | Value in range between [0, 1]                |  

</p>
</details>

These models are created in SQL Alchemy and are generated using alembic
