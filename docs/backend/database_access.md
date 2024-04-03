# Database access

## Overview
How we access and store data in the database

## Technologies used
- sqlalchemy (async)

## Description
Access to the database will be Encapsulated by a class: 'DataAccess'
by calling its member function we are able to communicate with the database.
To increase readability, the methods are divided into categories: UserAccess, CityAccess, ...

One special category is 'DeveloperAccess', its member functions are only supposed to be called by developers.
This can be used to create new types of buildings, troops, etc. 
This makes it easy for developers to add these features to the game. 
These tables will often be considered 'lookup tables' (user actions will not cause a change in its information).
This category can also provide methods for developers to do actions ordinary users are not allowed to do 
(ex. speeding up time, for debugging).

Other categories will have methods related to their category.
The dataAccess methods are asynchronous (to reduce response time) and so need to be called
from an asynchronous function. Using the 'DataAccess' method, all the other Access methods can be accessed 
(ex. ```DataAccess.UserAccess.createUser(params)```).

An overview of the current DataAccess categories:


| Category        | Purpose                                    | Extra Info                                                                                                                                           |
|:----------------|:-------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|
| AllianceAccess  | methods that manage alliances              |
| ArmyAccess      | methods that manage armies                 |
| BuildingAccess  | methods that manage buildings              | Everything with regards to a building can be managed from here, that also means all types of buildings                                               |
| CityAccess      | methods that manage cities                 |
| DeveloperAccess | methods that manage developer only actions | Every table whose entries are changed from this access, are meant as lookup tables. Changing these tables from another Access is highly undesirable. |
| MessageAccess   | methods that manage all message operations |
| PlanetAccess    | methods that manage Planets & Regions      | This Access method will mainly be used to create the surrounding environment of the game                                                             |
| TrainingAccess  | methods that manage training units         | This Access method will only take care of training units                                                                                             |
| UserAccess      | methods that manage User accounts          | 
| RankingAccess   | methods that manage ranking information    | User rankings will be done with regards to the amount of Solarium a player has/produces                                                              |
| ResourceAccess  | methods that manage resources of users     |                                                                                                                                                      |

## Issues
The entire database (tables and sequences) need to be present.

## Additional Information
