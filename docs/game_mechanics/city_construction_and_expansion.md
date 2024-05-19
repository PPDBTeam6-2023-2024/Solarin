# City Construction and Expansion

In the dynamic world of our game, players are tasked with the crucial role of constructing and expanding their own cities. This process is not only about growing a city in size but also about strategic planning and resource management to ensure sustainable development and progress.

## City Creation

The foundation of any great city starts with its creation. To establish a city, players will need to invest 4200 units of Solarium and provide space for 1024 citizens. This initial investment seeds the growth of your urban landscape, setting the stage for a thriving community.

### Costs and Requirements

- **Solarium (SOL)**: 25600 units
- **Population (POP)**: 1024 residents

This substantial upfront cost represents the resources and infrastructure required to lay down the roots of a new city. It is the first step in your journey to building a powerful metropolis.

## City Upgrade

As your city grows, upgrading its level becomes essential to accommodate increasing needs and expanding ambitions. Each city level represents an advancement in infrastructure, population capacity, and economic development. The maximum level a city can reach is level 5.

### City Upgrade Cost

To upgrade a city, the [General Upgrade Cost (GUC) formula](buildings_productions.md#general-upgrade-cost-guc) is applied to the initial city creation cost with as parameters the (initial_upgrade_cost,level). Note that creation cost is replaced by the initial upgrade cost in the GCUC calculation. This method ensures that the cost of city upgrade cost scales appropriately with its growth, reflecting the increased complexity and resource needs.

## City Upgrade Time Formula

### Formula
The time required to upgrade a city from one level to the next is calculated using the following formula:

Upgrade Time = floor(base × 1.15^(level + 1))

### Components

- `Upgrade Time`: The total time required to upgrade the city to the next level.
- `base`: The base time required for the level upgrade. This is a constant that sets the initial scale of time needed.
- `1.15`: This factor represents a 15% increase in the time required for each subsequent level.
- `level`: The current level of the city being upgraded.

### Purpose

The purpose of this formula is to provide a simple yet effective mechanism for increasing the challenge as the game progresses. Each level upgrade requires progressively more time, reflecting the increased complexity and resources needed to develop the city as it grows. This exponential growth ensures that the game remains engaging and strategically challenging, encouraging players to plan their upgrades and resource management carefully.

### Implications

- **Progressive Difficulty**: As players advance to higher levels, the increasing time demand adds to the game's difficulty, making each level achievement more satisfying.
- **Strategic Planning**: Players must think strategically about when and where to allocate their time and resources, as higher levels become significantly more time-intensive.

This formula balances simplicity with strategic depth, making it suitable for games where gradual progression and resource management are key gameplay elements.
