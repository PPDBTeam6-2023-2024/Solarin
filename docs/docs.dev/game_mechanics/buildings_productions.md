# Buildings & Production
## General Production Cost (GPC)

* Our base point bounds are currently $[0,499]$
* Current choice of $\text{rate}=5$ (how fast we want the GPC to increase)
* Production price per item type:
        * For product type tuple $\text{prod} = (b_1, ..., b_n)$:
                * $b_i \in [l, u] \cap \mathbb{N}$ is $i$th base point of the product
                * Each base point has lower and upper bound $l$ and $u$
                * $\text{basePrice}(\text{prod})$ is a function getting the base price of $\text{prod}$
                * $\text{GPC}(\text{prod})= \text{basePrice}(\text{prod}) \cdot{\left(\left\lfloor\dfrac{2\cdot\sum{b_i}}{n(l+u)}\right\rfloor\right)}^{\text{rate}}$ SOL
                * Example: production of a single land unit in the barracks:
                        * $\text{GPC(unit)}= 50\left(\left\lfloor\dfrac{\text{AP+DP+...+MS}}{1497}\right \rfloor\right)^5$ SOL
                * The currency type of GPC depends on the product type, therefore let's say the GPC is given in SOL (solarium) by default.
## Unit Stats Ranked
Calculating the units their stats can easily be done using the getUnitStatsRanked function
This function has the following formula: $base_value*grow_rate^level$
The grow_rate is configurable, by the developers. This should be greater than 1, to have the 
wanted effect. This makes sure that the units become drastically stronger the higher rank (level) the get

## Unit Train Cost
Units training costs are calculated using the following formula: $base_value*grow_rate^level$
This grow_rate can differ from the grow rate used for calculating the Unit Stats

## General Upgrade Cost (GUC)
* $\text{GUC(building)} = \left\lfloor\dfrac{\text{CC}\cdot(\text{level}+1}){2}\right\rfloor$ TF 
	* $\text{level}$ is the current (pre-upgrade) level of the building
	* $\text{CC}$ is the creation cost of the building
	* GUC and CC is given in Techforge (TF) currency by default

## General Upgrade Time (GUT)
* $\left\lfloor \text{TFC} \times 1.15^{\text{level} + 1} \right\rfloor
	* $\text{level}$ is the current (pre-upgrade) level of the building
	* $\text{TFC}$ is the Tech Forge cost for upgrading the building
	* GUT is thus dependent on the TF cost, determined by using the GUC formula

## General Production Rate (GPR)
* $\text{GPR(resource, building)}=\text{modifier(region, resource)} \cdot \text{baseRate(resource, building)}\cdot\text{level}^2 * (1+\text{Control Modifier(region, player)}*0.25)$ 
	* $\text{baseRate(resource, building)}$ is the amount of the resource produced in a given building per minute
	* $\text{modifier(region, resource)}$ is the modifier that is applied depending on the resource produced and the region where the building is located
    * $\text{Control Modifier (region, player) is a bonus multiplier that applies when a player controls all building instances within a region. This is set at a fixed value of +25% if the player is in control of the region.}$

## Building Types
A building can generally be upgraded up to level 10.
The capacity of a building is $\text{baseCapacity}\cdot\text{level}$
* Barracks
	* For training land units
		* $\text{basePrice}(\text{unit}) = 50$ SOL
		* $\text{baseCapacity(unit, barracks)}=20$
	* Creation Cost:
		* 550 TF
		* 100 POP

	* Training time will depend on the unit type
* Space Dock
	* For training space units 
		* $\text{basePrice}(\text{spaceUnit}) = 100$ SOL
		* $\text{baseCapacity(spaceUnit, spaceDock)}=30$
  	* Creation Cost:
		* 1250 TF 
		* 1000 Coal
  		* 250 Uranium
  	 	* 500 Oil

	* Training time will depend on the unit type
* Nexus
	* Produces: 
		* *Solarium (SOL)*
			* $\text{baseRate(SOL, nexus)}=600$
			* $\text{baseCapacity(SOL, nexus)}=5000$
		* *Techforge (TF)*
			* $\text{baseRate(TF, nexus)}=400$
			* $\text{baseCapacity(TF, nexus)}=5000$
	* Creation Cost:
		* 6500 TF
  		* 500 Uranium
    		* 500 Solarium 
	* The player begins with a free *Nexus*
* Farmpod
	* Produces *Rations (RA)*
		* $\text{baseRate(RA, farmpod)}=300$
		* $\text{baseCapacity(RA, farmpod)}=5000$
	* Creation Cost:
 		* 1200 TF
   		* 250 Minerals
     		* 50 Solarium 
* Cloning Chamber
	* Produces *Population (POP)*
		* $\text{baseRate(POP, cloningChamber)}=150$
		* $\text{baseCapacity(POP, cloningChamber)}=1000$
	* Creation Cost
		* 1500 TF
 	 	* 1000 Rations
    		* 250 Coal
      		* 100 Solarium
* Extractor
	* Produces:
		* *Minerals*
			* $\text{baseRate(minerals, extractor)}=500$
			* $\text{baseCapacity(minerals, extractor)}=1500$
		* *Oil*
			* $\text{baseRate(oil, extractor)}=500$
			* $\text{baseCapacity(oil, extractor)}=1500$
	* Creation Cost:
		* 3000 TF
  		* 150 Solarium
    		* 500 Coal
* Reactor
	* Produces *Uranium*
		* $\text{baseRate(uranium, extractor))}=100$
		* $\text{baseCapacity(uranium, extractor)}=550$
	* Creation Cost:
		* 10000 TF
  		* 250 Solarium
    		* 500 Minerals
  
* Oil Pump
	* Produces *Oil*
		* $\text{baseRate(oil, oil pump))}=400$
		* $\text{baseCapacit(yoil, oil pump)}=1600$
	* Creation Cost:
		* 3500 TF
  		* 50 Solarium
    		* 500 Coal
      
* Parlement
	* Produces *Influence*
		* $\text{baseRate(influence, parlement))}=100$
		* $\text{baseCapacity(influence, parlement)}=200$
	* Creation Cost:
		* 1500 TF
  		* 25 Solarium

* Solar Generator
	* Produces *SOL*
		* $\text{baseRate(SOL, solar generator))}=700$
		* $\text{baseCapacity(SOL, solar generator)}=5000$
	* Creation Cost:
		* 6800 TF
  		* 500 Coal
 
* Material Lab
	* Produces *TF*
		* $\text{baseRate(TF, material lab))}=700$
		* $\text{baseCapacity(TF, material lab)}=6000$
	* Creation Cost:
		* 9000 TF
  		* 150 Solarium
 
* Plant Growth Accelerator
	* Produces *RA*
		* $\text{baseRate(RA, plant growth accelerator))}=1500$
		* $\text{baseCapacity(RA, plant growth accelerator)}=10000$
	* Creation Cost:
		* 15000 TF
  		* 250 Uranium
 
* Electric Mine
	* Produces *Minerals*
		* $\text{baseRate(Minerals, electric mine))}=800$
		* $\text{baseCapacity(Minerals, electric mine)}=10000$
    * Produces *Coal*
		* $\text{baseRate(Coal, electric mine))}=200$
		* $\text{baseCapacity(Coal, electric mine)}=7000$
    * Produces *Oil*
		* $\text{baseRate(Oil, electric mine))}=30$
		* $\text{baseCapacity(Oil, electric mine)}=300$
	* Creation Cost:
		* 9000 TF
  		* 100 Solarium
 
* Solar Lab
    * Produces *TF*
        * $\text{baseRate(TF, material lab))}=100$
        * $\text{baseCapacity(TF, material lab)}=600$
    * Produces *SOL*
        * $\text{baseRate(TF, material lab))}=500$
        * $\text{baseCapacity(TF, material lab)}=4000$
    * Creation Cost:
        * 7000 TF
        * 500 Minerals
