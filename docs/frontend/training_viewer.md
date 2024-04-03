# training viewer

## Overview
A explanation of the frontend side of training units

## Technologies used
- React


## Description
To make training possible for users we have a component called 'TrainingViewer'
This component shows a view inside the city manager menu to be able to train troops.
This trainingmenu appears when you click in the building list on the building that is a 'barrack' type.
When you click again it will close

<br>![alt text](../images/image_training.png)

The first part of this menu is displaying the units that are currently in a training queue.
Each entry of this list has is a component: 'TrainingQueueEntry'. In case the list is too long to fit inside the screen, users can do 
a horizontal scroll using their mousewheel. The First entry of the queue will also automatically update its time remaining timer.
From the moment 1 units of the entry would be trained, the frontend-re syncs with the backend.

Another important part of this menu is to train new troops. Below the training queue list, a list of all the possible units that can be trained
are listed. When clicked on 1 of these units, on the right a slider appears. Using the slider, a user can choose how many troops it wants to train in 1 Queue.
It will also dynamically display the cost for training these units.

The list of trainable units are part of the 'TrainingOptionBar' component.
The slider, cost display, Train Units are part of the 'TrainOptionAdder' component.

In regard to communicating to the backend, It can request the training queue of a building, send a new troop it wants train. And retrieve the troop creation cost
for dynamically change the value based on the slider.


## Issues


## Additional Information
