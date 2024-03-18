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
			* $\text{modifier(arctic, oil)} = 0.8$
* Desert Region:
	* A very hot region with desert.
	* Common Resources:
		* Oil
			* $\text{modifier(desert, oil) = 1.4}$
		* Uranium
			* $\text{modifier(desert, uranium) = 1.2}$
	* Uncommon resources:
		* Techforge
			* $\text{modifier(desert, TF) = 0.8}$
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
* Plain Region:
	* A generally treeless, flat region.
	* Common Resources:
		* Rations
			* $\text{modifier(plain, RA)} = 1.5$
		* Coal
			* $\text{modifier(plain, coal) = 1.1}$
	* Uncommon Resources:
		* Techforge
			* $\text{modifier(plain, TF) = 0.8}$
## Planet Types

* Arctic Planet
	* Arctic regions
	* Alpine regions
* Desert Planet
	* Desert regions
	* Plain regions
* Tropical Planet
	* Plain regions
	* Alpine regions
