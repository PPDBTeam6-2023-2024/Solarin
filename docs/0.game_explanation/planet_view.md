# PlanetView

The view of a planet looks something like the image below:
<br>![alt text](../images/planet_view.png)
A planetView contains regions (marked by the black lines). Each region is just represented by a point on the map,
deciding in which region somthing is, can simply be done by checking which region point is the closest.

Planets have their own types, and so do regions. Certain regions can only exist on certain planet types.
We also see cities, by clicking on a city the city menu will open (at least if you are the owner of this city).

We Also see armies on the map. Websockets make it possible to see army movement and changes live, but be aware movement 
takes some time, so you might not see this visually.
