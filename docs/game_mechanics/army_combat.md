# Army Combat 

During army combat the winner will be determined by a formula

* Unit strength
	
	* For calculating the strength of an army the following formula is used: $\text{strength(unit)}=\dfrac{\text{rank(unit)}\cdot\text{mean(P)}}{250}$
        * $\text{P} = ( \text{AP, DP, ..., CDP})$
        * Take into account city defense and defense will be scaled by a weight so the resulting $final defense = w*city_defense*(1-w)*defense$. This is so we their is a difference (with regards to stats) between fighting between armies and fighting in a city. The same counts for attack and city attack.
        * Recovery is scaled by a modifier < 1, to make sure that the 'recovery' stat does not influence too much of the battle outcome.
    *  $\text{cityStrength(unit)}=\dfrac{\text{rank(unit)}\cdot\text{mean(CW(P))}}{250}$
		* $\text{CW(P)} = ( \text{CW(AP), CW(DP), ..., CW(CDP)})$
		* $\text{CW(point)} = \begin{cases}\text{point}\text{ if isCity(point)}=1\\(0.5\cdot\text{point})\text{ if isCity(point)}=0\end{cases}$
			* Example: $\text{CW(CDP)}=\text{CDP},\text{CW(DP)}=0.5\cdot\text{DP}$
* Army strength
	* $\text{strength(army)}=\text{mean}(\text{strength(unit}_1),...,\text{strength(unit}_n))$ 
	* $\text{cityStrength(army)}=\text{mean}(\text{cityStrength(unit}_1),...,\text{cityStrength(unit}_n))$ 
## Battle 
A battle is initiated when player 1 decides to attack player 2 by either directly attacking an army not stationed in a city or attacking the player's city.

(*TODO*: add towers, turrets strength to cityBattle and give weights to attacking and defending)
* $\text{battle}(\text{army}_1, \text{army}_2)=\text{max}\left[\text{rand}_1\cdot\text{strength}(\text{army}_1),\text{rand}_2\cdot\text{strength}(\text{army}_2)\right]$
* $\text{cityBattle}(\text{army}_1, \text{army}_2)=\text{max}\left[\text{rand}_1\cdot\text{cityStrength}(\text{army}_1),\text{rand}_2\cdot\text{cityStrength}(\text{army}_2)\right]$
* $\text{rand}_1, \text{rand}_2 \in \left[\frac{1}{2}, \frac{3}{2}\right] \sim N(1,0.1)$ 
## Post-Battle Recovery
The Post-Battle Recovery gives information about how many troops are reamining after an attack.

We define 2 ratio's:

* $PBR ratio = \dfrac{\text{winning PBR}}{\text{losing PBR}}$
* $strength ratio = \dfrac{\text{winning strength}}{\text{losing strength}}$ (This will almost always be > 1 (unless the random factor changes the outcome to much) )


$\text{armySurvival} \in \left[0,1\right] \sim N(\text{PBR ratio}\cdot\left(1-\dfrac{1}{\text{strength ratio}}\right), 0.1)$ where $\left\lfloor\text{armySurvival}\cdot\text{numOfUnits(army)}\right\rceil$ is the number of units surviving after a battle.

## Army movement
Armies can move between 2 positions, but it will take some time. The time needed will depend on the speed of an army
The formula we use for calculating the duration is as follows:

* $mapCrossTime = \dfrac{1000}{army speed}\cdot 3600$ (The 3600, just makes sure we have hours)
* $duration =  mapCrossTime\cdot distance$