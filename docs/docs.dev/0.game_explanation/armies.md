# Armies
Controlling armies is a vital part of our strategy game
<br>![alt text](../images/army_details.png)
When we select an army (assuming we select an army controlled by the user self)
We can click 2 buttons: 'Move To' and 'Details'.
The Move To can be selected, when we click after on a place on the map, our army will move to the
provided position (using IDLE long times, but does also update live). When we click details another window appears.
'Create City' makes it possible to create a new city on the position of the army. 

If another city is to close, a pop-up message will appear (global notification) that another city is too close to
create a new city.

The stats visualize the stats of the army, which will be used to calculate battle outcomes.
We can also see which units are part of this army.

An army can also attack other armies/cities by clicking on that army/city when deciding the movement.
When the army arrives, it will calculate the combat results, and remove the defeated armies/ change city ownership accordingly.

When an army clicks on its own army it will move towards that army and when it arrives will merge both armies.
When an army moves to its own city, it will enter the city.
To indicate which action will be done, Cursor indications are given when hovering over another city/army

We chose to do army actions with OnArrive events.
This means that we keep track of when an army would arrive at the selected location
When it arrives, we will trigger an 'onArrive' event, and to the necessary checks.

### Splitting up an army
If an army consists of multiple troops, it may be desirable to split up the army. 
This can be done by selecting the troops which you wish to split off, and press the "split army" button.
<br>![alt text](../images/split_army_on_map.png)


<br>![alt text](../images/fleet.png)<br>
Fleets, which are armies with at least one mothership unit,  are just like armies in terms of combat, merging, moving, viewing stats, etc... However, they can also enter and exit planets. 
