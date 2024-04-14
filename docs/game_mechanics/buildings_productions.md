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

## General Production Rate (GPR)
* $\text{GPR(resource, building)}=\text{modifier(region, resource)} \cdot \text{baseRate(resource, building)}\cdot\text{level}^2$ 
	* $\text{baseRate(resource, building)}$ is the amount of the resource produced in a given building per minute
	* $\text{modifier(region, resource)}$ is the modifier that is applied depending on the resource produced and the region where the building is located
## Building Types
A building can generally be upgraded up to level 10.
The capacity of a building is $\text{baseCapacity}\cdot\text{level}$
* Barracks
	* For training land units
		* $\text{basePrice}(\text{unit}) = 50$ SOL
		* $\text{baseCapacity(unit, barracks)}=20$
	* Creation Cost:
		* 550 TF

	* Training time will depend on the unit type
* Space Dock
	* For training space units 
		* $\text{basePrice}(\text{spaceUnit}) = 100$ SOL
		* $\text{baseCapacity(spaceUnit, spaceDock)}=30$
	* 1250 TF Creation Cost
	* Training time will depend on the unit type
* Nexus
	* Produces: 
		* *Solarium (SOL)*
			* $\text{baseRate(SOL, nexus)}=5$
			* $\text{baseCapacity(SOL, nexus)}=500$
		* *Techforge (TF)*
			* $\text{baseRate(TF, nexus)}=15$
			* $\text{baseCapacity(TF, nexus)}=5000$
	* Creation Cost:
		* 6500 TF
	* The player begins with a free *Nexus*
* Farmpod
	* Produces *Rations (RA)*
		* $\text{baseRate(RA, farmpod)}=30$
		* $\text{baseCapacity(RA, farmpod)}=5000$
	* 1000 TF Creation Cost
* Cloning Chamber
	* Produces *Population (POP)*
		* $\text{baseRate(POP, cloningChamber)}=15$
		* $\text{baseCapacity(POP, cloningChamber)}=5000$
	* Creation Cost
		* 1500 TF
* Extractor
	* Produces:
		* *Minerals*
			* $\text{baseRate(minerals, extractor)}=10$
			* $\text{baseCapacity(minerals, extractor)}=1000$
		* *Oil*
			* $\text{baseRate(oil, extractor)}=10$
			* $\text{baseCapacity(oil, extractor)}=1000$
	* Creation Cost:
		* 3000 TF
* Reactor
	* Produces *Uranium*
		* $\text{baseRate(uranium, extractor))}=15$
		* $\text{baseCapacity(uranium, extractor)}=250$
	* Creation Cost:
		* 10000 TF
 

