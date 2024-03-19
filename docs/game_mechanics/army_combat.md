# Army Combat 
* Unit strength
	* $\text{strength(unit)}=\dfrac{\text{rank(unit)}\cdot\text{mean(P)}}{250}$
        * $\text{P} = ( \text{AP, DP, ..., CDP})$
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
$\text{armySurvival} \in \left[0,1\right] \sim N(\dfrac{\text{PBR}}{\text{upperBound(PBR)}}, 0.1)$ where $\left\lfloor\text{armySurvival}\cdot\text{\#units}\right\rceil$ is the number of units surviving after a battle for both players.
