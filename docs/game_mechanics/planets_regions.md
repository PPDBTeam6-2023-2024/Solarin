# Planets & Regions
## Regions
$\text{modifier(region, subject) = x}$
* $x \in \mathbb{R}^+$
### Region Types
* Arctic Region
	* A cold region with snow.
	* Common Resources:
		* Coal
			* $\text{modifier(arctic, coal) = 1.2}$
		* Minerals 
			* $\text{modifier(arctic, minerals) = 1.3}$
	* Uncommon Resources:
		* Oil
			* $\text{modifier(arctic, oil) = 0.8}$
        * Rations
            * $\text{modifier(arctic, minerals) = 0.6}$
* Polar Region
	* A very cold region with snow.
	* Common Resources:
		* Coal
			* $\text{modifier(Polar, coal) = 0.8}$
		* Minerals 
			* $\text{modifier(Polar, minerals) = 1.4}$
	* Uncommon Resources:
		* Oil
			* $\text{modifier(Polar, oil) = 0.5}$
        * Rations
            * $\text{modifier(Polar, RA) = 0.8}$
        
* Desert Region:
	* A very hot region with desert.
	* Common Resources:
  		* Solarium
			* $\text{modifier(desert, solarium) = 1.1}$
		* Oil
			* $\text{modifier(desert, oil) = 1.4}$
		* Uranium
			* $\text{modifier(desert, uranium) = 1.2}$
	* Uncommon resources:
		* Techforge
			* $\text{modifier(desert, TF) = 0.8}$
        * Rations
            * $\text{modifier(desert, RA) = 0.5}$
* Alpine Region:
	* A region with a lot of mountains.
	* Common Resources:
		* Minerals
			* $\text{modifier(alpine, minerals) = 1.4}$
		* Techforge
			* $\text{modifier(alpine, TF) = 1.2}$
	* Uncommon Resources:
		* Uranium
			* $\text{modifier(alpine, uranium) = 0.8}$
        * Rations
            * $\text{modifier(alpine, RA) = 0.9}$
* Plain Region:
	* A generally treeless, flat region.
	* Common Resources:
		* Rations
			* $\text{modifier(plain, RA) = 1.6}$
		* Coal
			* $\text{modifier(plain, coal) = 1.1}$
	* Uncommon Resources:
		* Techforge
			* $\text{modifier(plain, TF) = 0.8}$
* Taiga Region:
	* A region filled with aggregation common for cold regions
	* Common Resources:
		* Techforge
			* $\text{modifier(taiga, TF) = 1.5}$
	* Uncommon Resources:
        * Oil
            * $\text{modifier(taiga, oil) = 0.8}$
        * Rations
            * $\text{modifier(taiga, RA) = 0.7}$
        * Uranium
			* $\text{modifier(taiga, uranium) = 1.3}$
* Savannah Region:
	* Long stretching plains in a hot climate, with barely any trees
	* Common Resources:
		* Techforge
			* $\text{modifier(savannah, TF) = 1.05}$
        * Solarium
			* $\text{modifier(savannah, SOL) = 1.1}$
	* Uncommon Resources:
        * Oil
            * $\text{modifier(savannah, oil) = 0.8}$
        * Rations
            * $\text{modifier(savannah, RA) = 0.7}$
        * Uranium
			* $\text{modifier(savannah, uranium) = 0.4}$
* Steppe Region:
    * regions covered with dry grass
	* Common Resources:
		* Rations
            * $\text{modifier(steppe, RA) = 1.3}$
        
	* Uncommon Resources:
  		* Solarium
			* $\text{modifier(steppe, SOL) = 0.9}$
        * Uranium
			* $\text{modifier(steppe, uranium) = 0.7}$
      
* Rainforest Region:
    * region filled with large trees, in these regions there is a lot of rainfall 
	* Common Resources:
		* Rations
            * $\text{modifier(rainforest, RA) = 1.8}$
        * Minerals
			* $\text{modifier(rainforest, minerals) = 1.2}$
	* Uncommon Resources:
        * Uranium
			* $\text{modifier(rainforest, uranium) = 0.7}$
        * Oil
            * $\text{modifier(rainforest, oil) = 0.5}$
        * Techforge
			* $\text{modifier(rainforest, TF) = 0.6}$
        * Solarium
			* $\text{modifier(rainforest, SOL) = 0.7}$
* Coast Region:
    * region which has some water near/in it
	* Common Resources:
		* Rations
            * $\text{modifier(coast, RA) = 1.2}$
        * Uranium
			* $\text{modifier(coast, uranium) = 1.4}$
	* Uncommon Resources:
        * Techforge
			* $\text{modifier(coast, TF) = 0.7}$
        * Solarium
			* $\text{modifier(coast, SOL) = 0.9}$
        * Minerals
			* $\text{modifier(coast, minerals) = 0.6}$
          
* Magma Region:
    * region filled with hot stones, and warm magma
	* Common Resources:
  		* Minerals
			* $\text{modifier(magma, minerals) = 2.5}$
        * Uranium
			* $\text{modifier(magma, uranium) = 1.8}$
        * Solarium
			* $\text{modifier(magma, SOL) = 1.1}$
	* Uncommon Resources:
        * Oil
            * $\text{modifier(magma, oil) = 0.8}$
        * Rations
            * $\text{modifier(magma, RA) = 0.1}$
        * Techforge
			* $\text{modifier(magma, TF) = 0.3}$

* Volcanic Region:
    * region filled with warm stones
	* Common Resources:
  		* Minerals
			* $\text{modifier(volcanic, minerals) = 1.6}$
        * Uranium
			* $\text{modifier(volcanic, uranium) = 1.4}$ 
        * Oil
            * $\text{modifier(volcanic, oil) = 1.6}$
	* Uncommon Resources:
        * Rations
            * $\text{modifier(volcanic, RA) = 0.2}$
        * Techforge
			* $\text{modifier(volcanic, TF) = 0.7}$

* Silicaat Region:
    * region filled with precious minerals
	* Common Resources:
  		* Minerals
			* $\text{modifier(silicaat, minerals) = 3.1}$
	* Uncommon Resources:
		* Uranium
			* $\text{modifier(silicaat, uranium) = 0.7}$
        * Oil
            * $\text{modifier(silicaat, oil) = 0.6}$
        * Rations
            * $\text{modifier(silicaat, RA) = 0.7}$
        * Techforge
			* $\text{modifier(silicaat, TF) = 0.9}$
        * Solarium
			* $\text{modifier(silicaat, SOL) = 0.9}$
          
* Dark forest Region:
	* A forest without much light 
	* Common Resources:
  		* Rations
            * $\text{modifier(dark forest, RA) = 1.1}$
	* Uncommon Resources:
        * Solarium
			* $\text{modifier(dark forest, SOL) = 0.2}$
        * Techforge
			* $\text{modifier(dark forest, TF) = 0.9}$
        
* Valley of shadow Region:
    * What or who lives in these regions is still unknown, while difficult to see because of the darkness, the region is full of richness
	* Common Resources:
  		* Techforge
			* $\text{modifier(valley of shadow, TF) = 1.5}$
        * Uranium
            * $\text{modifier(valley of shadow, uranium) = 1.1}$
        * Minerals
			* $\text{modifier(valley of shadow, minerals) = 1.1}$
	* Uncommon Resources:
        * Solarium
			* $\text{modifier(plain, SOL) = 0.3}$
        
## Planet Types

* Arctic Planet
	* Arctic regions
    * Polar regions
    * Taiga Regions
	* Alpine regions
* Desert Planet
	* Desert regions
	* Plain regions
    * Savannah regions
    * Steppe regions
* Tropical Planet
	* Plain regions
	* Alpine regions
    * Rainforest regions
    * Coast regions
* Red Planet
    * Magma regions
    * Volcanic regions
    * silicaat regions
* Dry Planet
    * Desert regions
    * Savannah regions
    * Silicaat regions
    * Steppe regions
* Shadow planet
    * Dark forest 
    * Valley of shadow regions
    * Silicaat regions