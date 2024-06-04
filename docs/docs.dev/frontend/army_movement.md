# Army Movement

## Overview
Moving armies from point a to point b by selecting armies and clicking on the spot to move.
When an army movement clicks on another army/ city, something will happen when they arrive
This means the following: 

- Army to Army (Own army): Merge the 2 armies on arrival
- Army to Army (Enemy army): Army attacks other army on arrival
- Army to City (Own city): Army enters the city on arrival
- Army to City (Enemy city): Army attacks city on arrival

## Technologies used
- ReactJS

## Description
State arrays are stored on the frontend to know which armies are currently selected under "Move To". Furthermore the armies can be seen moving smoothly after choosing their destination. This is done by having set up a code that runs every interval to actually move the army images dynamically. 
Depending on where the user clicks on the map, the army will move to this position and may or may not do an on arrive action.
## Issues

## Additional Information
