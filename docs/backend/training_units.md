# Training Units

## Overview
Explanation about how units are being trained on the backend side

## Description
In the routers > unitManagement > router is the router that handles all the endpoints for training units
is barrackBuilding specific, meaning that training has its own training queue for each building that is a Barrack type.

TrainingAccess is specific database access for training units.
It can be used to add new units to the training queue. Each building Instance has an attribute 'last checked'.
This indicates when a building was last checked. To check the IDLE progress of the training of units, we will trigger a check
who uses the current time and the last checked time to determine a delta time. This delta time will be subtracted from the training time
and will leave the remaining time. In case the delta time is bigger than the time needed to train, These units will be trained and the queue entry will be removed.
A queue entry contains an amount of troops, Even when de queue is not yet finished entirely, Some troops of this entry can already be trained.
When trained these troops will automatically be assigned to the provided army.

Units will currently be added to the lowest id army that is inside a city
When no army is inside the city, automatically a new army will be created

## Issues


## Additional Information
