## Points
A point is a natural number and always bounded by the interval [0,499]
### Point Classification
* Very Low: [0, 49]
* Low: [50,149]
* Moderate: [150,349]
* High: [350, 449]
* Very High [450, 499]
### Unit Strength 
* $\text{strength(unit)}=\text{rank(unit)} \cdot \dfrac{\sum{b_i}}{|\text{BP}|}$
	* $b_i \in \text{BP}$
	* $\text{BP} = \\{ \text{AP, DP, ..., AMS} \\} $
	* $\text{rank(unit) is the current level of the unit}$
### Point Types
* AP: Attack Points
    * The general attack power of a unit
* DP: Defense Points
    * The general defense power of a unit
* CAP: City Attack Points
    * The attack power of a unit in city battles
* CDP: City Defense Points
    * The defense power of a unit in city battles
* PBR: Post-Battle Recovery
    * The general probability of survival after a participated battle of a unit
* AMS: Average Movement Speed
    * The average movement speed of a unit

## Units
* Spec
	* Specialization of the unit: land or space
* Base points
	* The points a unit starts with
* Current points
	* Base points of the unit times current rank of the unit
### Regular Units

* Assault Unit
    * Spec: Land
    * Base Points:
        * (Moderate) 250 AP
        * (Moderate) 250 DP
        * (Moderate) 250 CAP
        * (Moderate) 250 CDP
        * (Moderate) 250 PBR
        * (Moderate) 250 MS
* Tank Unit
    * Spec: Land
    * Base Points:
        * (Low) 149 AP
        * (High) 350 DP
        * (Low) 149 CAP
        * (High) 300 CDP
        * (Moderate) 250 PBR
        * (Low) 149 MS
* Assassin Unit
    * Spec: Land
    * Base Points:
        * (High) 350 AP
        * (Low) 149 DP
        * (Moderate) 250 CAP
        * (Low) 149 CDP
        * (Moderate) 250 PBR
        * (High) 350 MS
* Medic Unit
    * Spec: Land
    * Base Points:
        * (Moderate) 200 AP
        * (Moderate) 200 DP
        * (Moderate) 200 CAP
        * (Moderate) 200 CDP
        * (High) 350 PBR
        * (Moderate) 250 MS
* Fighter Unit
    * Spec: Space
    * Base Points:
        * (High) 350 AP
        * (Moderate) 200 DP
        * (Low) 149 CAP
        * (Moderate) 200 CDP
        * (Moderate) 250 PBR
        * (High) 350 MS

* Bomber Unit
    * Spec: Space
    * Base Points:
        * (Moderate) 250 AP
        * (Low) 149 DP
        * (High) 350 CAP
        * (Low) 149 CDP
        * (Moderate) 250 PBR
        * (High) 350 MS
