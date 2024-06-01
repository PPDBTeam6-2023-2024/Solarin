# Maintenance
## Overview
Explanation how maintenance costs are checked and applied for cities and armies

## Description

Maintenance of armies and cities is an IDLE mechanic.
Therefor, each user has an attribute 'last_maintenance_check'. This stores the timestamp when the last maintenance check did occur.
Having this information, we can calculate the delta time = current_time - last time.
Based on this delta time we can do calculations with regards to maintenance cost.
Looking at game mechanics you can find how the maintenance costs are calculated.
Our resource cost at a given time for each resource m would be: m*delta time /per hour.
If we do not have enough resources, the following will happen:
First we will check the armies, if an army does not have enough maintenance, of those troops using this resource each hour 10%
will die.

When we still miss resources, we will give effect on the cities. When a city can't pay the maintenance cost,
all buildings in that city will be removed.



