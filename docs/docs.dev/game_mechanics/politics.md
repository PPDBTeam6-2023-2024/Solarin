# Politics and modifiers

The user can influence how their society evolves through decisions in the political menu. Each type of society has an impact on a set of modifiers. 
How big this impact is depends on how much the user leans into that kind of society. 
Wo keep track of how much a user leans into the different kinds of societies with separate numbers between 0 and 1.
We then multiply these values with some constants we defined to get an impact on a specific modifier. 


## Types of Societies


### Anarchism
A society that is in a general state of disarray.

### Democratic
A society that emphasizes individual freedoms and equality.

### Theocracy
A society governed by religious leaders or based on religious principles.

### Technocracy
A society that is governed by scientists, engineers, and other technical experts.

### Corporate State
A society that is governed by corporate entities or heavily influenced by corporate interests.

### Authoritarian
A society characterized by strong central power and limited political freedoms.


## Modifier calculation
These are the formulas we use to calculate the modifiers, all of these are limited to [-30%, +30%] to keep the game balanced and enjoyable.

- **Resource Production**

$\text{Resource Production} = \text{anarchism} \times 10 + \text{democratic} \times 3 - \text{theocracy} \times 10 - \text{technocracy} \times 5 + \text{corporate\_state} \times 20 $

- **Upgrade Speed**

$ \text{Upgrade Speed} = \text{technocracy} \times 25 + \text{democratic} \times 20 - \text{authoritarian} \times 15 - \text{theocracy} \times 20 - \text{corporate\_state} \times 10 $

- **Army Strength**

$ \text{Army Strength} = \text{authoritarian} \times 30 - \text{anarchism} \times 20 + \text{theocracy} \times 15 - \text{democratic} \times 10 $

- **Training Time**

$ \text{Training Time} = -\text{authoritarian} \times 20 - \text{technocracy} \times 15 - \text{corporate\_state} \times 10 + \text{theocracy} \times 10 $

- **Army Movement Speed**

$ \text{Army Movement Speed} = \text{anarchism} \times 10 - \text{corporate\_state} \times 30 - \text{theocracy} \times 5 $