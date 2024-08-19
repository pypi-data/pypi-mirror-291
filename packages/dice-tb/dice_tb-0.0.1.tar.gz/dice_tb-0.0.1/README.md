# Dice Package

This is a simple dice package which has the type Dice which can have a value between 1 and the number of sides. 

# Importing

## Import dice
You can import the dice package by:
``` 
from dice_tb import dice
```

## Import dice_simulation
You can import the dice package by:
``` 
from dice_tb import dice_simulation
```

# Uses
How you can use this package.

## Using dice
How you can use dice.

### Instantiate dice.Dice
You can use the dice using:
```
d1 = dice.Dice()
```
which has the value:
```
d1.sides
d1.value
```
of 6 and -1.

Or you can use the dice by setting the sides using:
```
d2 = dice.Dice(sides=20)
```
which has the value:
```
d2.sides
d2.value
```
of 20 and -1.

### Using roll
You can roll a dice using:
```
d3 = dice.roll(d1)
```
which generates a new dice d3 with different values.

You can roll a dice using a seed:
```
d4 = dice.roll(d1, seed=5)
d5 = dice.roll(d4, seed=5)
```
where d4.value == d5.value.

## Using dice_simulation
How you can use dice.

You can simulate dice roll for a simple game that computes the sum of 2 six-sided dice, where the player starts with a $100 bankroll, each roll you bet $1, and if the sum is 7, 11, or a pair then you make $2 otherwise you lose $1.

The outcomes of the set of rolls.

You can run the Monte Carlo Simulation using:
```
monte_carlo_simulation = dice_simulation.MonteCarloSimulation(None, dice_simulation.setup_before_all_simulations, dice_simulation.simulation_loop_body, dice_simulation.display)
monte_carlo_simulation.run_simulation()
dice_simulation.monte_carlo(1000)
```
