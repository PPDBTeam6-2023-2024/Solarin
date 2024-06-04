# Army Combat

## Overview
Explanation how combat of an army works


## Description
The combat of an army exists of 2 parts. The first part is detecting when combat needs to occur, the second part is to do the combat calculations and change the
stored data accordingly.

For detection of combat we use the Table 'onArrive'. This has polymorphic children: 'AttackCity', 'AttackArmy', ....
When a user decides to attack an army/city it will store that information in these tables. When our army later arrives on
its destination, we check these tables. If we find a matching table entry (with our arrived army) we will execute the calculations.
Armies cannot attack their own armies,cities or those of their allies

Army movement on a planet is done with websockets to get real time updates, to be able to directly update combat when players are online,
We will calculate the remaining time needed before an army arrives (and would start the combat). We make an async tasks with a delay so it only does the 
check after the army would arrive. If the entry does not exist anymore by then, the check will just ignore it.
When the check occurs, the websocket will send a 'reload' message to the clients, so frontend can reload de cities and armies, to
keep it in sync. Doing the check occurs in the file 'ArriveCheck.py'. Using websockets, an army can also provide whether it is going to attack an army/city using
the same request it uses to change movement.

Doing the combat calculations (ArmyCombat.py): We use the formula's described in game_mechanics army_combat.
We also apply the losses to each troop entry of the winning army. Losing armies will be removed, and when a city failed to defend himself
the attacker will become owner of the city. And the conquering army will enter the city. 

Armies that are presented in a city while it is attacked, will help defending the city, but will take losses when the defense is victorious. (if it loses they will just be removed).

Another aspect of controlling armies, is being able to enter cities with your army, and to merge armies.
This uses the same system as the attack: 'onArrive' events. This has 2 polymorphic children: 'MergeArmies', 'EnterCity', that store whether
to merge armies / enter an city when the army arrives at its destination.

All the on Arrive event handeling occurs in 'ArriveCheck', this will make sure the right action is triggered.
