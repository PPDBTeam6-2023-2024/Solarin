# Solarin
Our game I an IDLE strategy game. The user playing our game will control a space civilization of an alien race.
Cities will be founded, and armies will be raised. Users will be able to fight each other using these armies, and try to conquer 
each other their cities. Each city has buildings, that can produce resources, train troops, ...
Users start on a single planet, where they can grow their civilization. Later on, users will be able to travel to other distant planets.
The goal of our game is to grow your civilization as much as possible, by conquering and working together.
The other documentation files inside the `/general_explanation` will shed some more light about the most important
game features. 

## IDLE mechanics
Our IDLE components mainly consist of time delays, and duration.
- Buildings that produce a certain resource, have a production of X amount fo resources /hour (So the user needs to wait some time).
- Training Troops for your armies will take time.
- Moving Armies, will take a couple hours depending on the distance.
- Adding/upgrading buildings will need some time to do the construction.

## Strategy mechanics
Our game will have a great deal of strategy and conquest. 
A lot of tactical decisions will be made with regards to managing cities, waging war, and working together with 
fellow users. The amount of time a user spends growing a civilization will give the user an advantage, 
but strategy will make it possible to overcome the head start of other players. 
Players will of course be able to make an account and login after a while to see their IDLE progress.

We make the strategy aspect possible by letting the user make a lot of decisions that may or may not help the user.
Modifiers will be provided to make the decision taking more important (ex. based on the type of region  the production rate modifier might change).

## Features:

### planet map
In our game we have a map that visualizes a planet.
- Visualization of a planet map
- Automatic generation of the planet + planet regions using voronoi
- Use planet to do actions on that planet

### planet regions
Each planet exists of multiple regions
- giving modifiers (to production of specific resources) to city situated on a region
- Extra modifier when the user has full and only control of the region

### Cities 
Cities can be created on a planet and be used to produce resources, train units,...
- Visualization of city on planet map
- City menu displayed when city clicked. Containing (Current buildings, new buildings (that we can build)), army in city info, and city info.
- Category selection TAB to change what the user sees
- Use cities to IDLE produce resources
- use cities to IDLE train troops
- IDLE upgrade the city
- IDLE upgrade the buildings inside a city
- Build new buildings inside the city
- Display city information, its region modifiers, population, maintenance cost
- Visualization of each building inside the city (using an image) on hover
- Change city visualization based on city rank
- Change city production/training level based on building level
- Cities can have Towers and Walls to improve the city its combat stats
- When Space Dock is build, planet is visible to other players too
- City combat stats visualized
- Click outside city menu widget to close menu
- Make upgrade/build buttons not clickable when not enough resources

### Armies
- Be able to have armies
- Create a city using an army
- Move an army across the planet map (IDLE takes long time)
- Armies can attack other armies and cities
- Armies of the same user can merge with each other
- Armies can enter its own city
- Armies can be split, both when in and out of city.
- Troops that are trained are added to the army inside the city
- Armies can be moved through space by having a 'mothership' troop.
- Army stats can be seen as details
- Display which troops are part of this army + rank + amount
- Make part of the army info hidden for other users
- Army general can be assigned giving the users bonuses based on the general and the user its political stance
- Army maintenance can be seen both in and out of a city
- visualize a line for army movement
- Combat Notifications about the battle results
- Army combat based on formula (can occur IDLE)

### Galaxy map 
A 3D view of the galaxy provides the visualization of the planets in space.
- 3D visualization
- Uses Generation algorithm to generate the position of the new planets (Fibonacci Spiral)
- Only allow a user to visit a planet when the user has something on that planet
- Only display planets that can be visible
- Another planet is only visible if it build a 'space dock'
- Transport armies through space (using a 3d FLEET)
- visualize a line for fleet movement
- Button to go to galaxy view
- Double click on planet to go to planet view

### Trading
Users can trade with each other (in same alliance)
- Being able to trade resources
- Cancel your own trade
- Accept someone else its trade
- use filters to filter for specific resources
- Create trades

### Chat
The communication aspect of the game
- Being able to send friend requests
- Being able to accept and reject friend requests
- Being able to send dm's to another player
- Being able to request to join an alliance
- Accept/Reject alliance requests
- Kick someone from the alliance
- Leave the alliance
- Open the alliance chat (chat between all users in the alliance)
- See a ranking between players, based on their amount of solarium a user has

### Resources
The user is able to obtain resources
- Visualization of the current resources
- Actions require certain resources, and they cannot be done when not enough resources
- Production buildings produce different resources
- Different resources used for different things

### maintenance Cost
Let Cities and armies have maintenance cost (resources /hour)
- Live update maintenance cost on resources
- Visualize maintenance cost for army in/out of city and for city itself
- When not enough resources, troops starve: losing troops, and buildings are being removed (slowly)

### Game Over
game over detection
- respawn the user when game over (no cities and armies)
- Added Game restart button in settings menu

### Hideable
making certain UI components hidable
- make it possible to hide certain UI components (in case you need access a city just hiden by this component)

### Settings
having a settings menu
- Provide restart button
- Let the user customize the visual UI Colors
- Button to make these colors persistent
- Click outside widget to close

### Side Menu
Small button right top corner
- Option to open setting menu
- Sign out button

### Planet switcher
Switch between planets the user has an army/city on
- Use switcher arrows to quickly switch between planets

### ProfileView
When we click on profile button (left bottom), we get the profile view, 
that displays useful user information
- Category selection Tab
- Visualize list of all the cities of the user (Cities Tab)
- Visualize list of all the armies of the user (Armies Tab)
- Go to politics menu using Politics tab

### Politics
By changing the ideology, the user gets different modifiers
- Visualize Radar graph of the ideology spectrum of the user
- Visualize modifiers based on current ideology
- Provide decisions that can be taken to make changes in the ideology
- Modify army general stats based on political stance
- Change general modifiers based on political stance

### Training
training of troops
- Let troops be trained
- Training queue for each barrack, which will IDLE train troops
- Slider to select how many troops need to be trained
- Display the stats of the troop (corres with amount trained) when we would train these troops
- Display the costs of training these troops