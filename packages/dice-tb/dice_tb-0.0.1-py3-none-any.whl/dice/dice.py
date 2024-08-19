# imports random module for random number generation for random dice values
import random

# imports numpy random to randomize the seed
import numpy

# imports dataclass which is used to create datatypes for dice and state
from dataclasses import dataclass

from typing import Union


@dataclass
class Dice:
    sides: int = 6
    value: int = -1
    

    def __post_init__(self):
         if type(self.value) == int and type(self.sides) == int:

             if 0 < self.sides:

                 if -1 <= self.value <= self.sides:
                     pass

                 else:
                     raise ValueError() 

             else:
                 raise ValueError()

         else:
             raise TypeError()


    @classmethod
    def roll(cls, dice, seed: Union[int,None] = None):
        if type(dice) == Dice:

            if type(seed) == int or seed is None:

                if seed is None:
                    seed = numpy.random.rand()

                    my_random = random.Random(seed)

                    # shuffles the decks
                    dice_value = my_random.randint(1, dice.sides)

                    return Dice(sides=dice.sides, value=dice_value)

                else:
                    my_random = random.Random(seed)

                    # shuffles the decks
                    dice_value = my_random.randint(1, dice.sides)

                    return Dice(sides=dice.sides, value=dice_value)

            else:
                raise TypeError()
                
        else:
            raise TypeError()


def test():
    d1 = Dice()
    d2 = Dice(sides=20)

    # side test
    print(d1.sides == 6)
    print(d2.sides == 20)

    # value test
    print(d1.value == -1)

    # roll test
    print(1 <= Dice.roll(d1).value <= d1.sides)
    print(1 <= Dice.roll(d2).value <= d2.sides)

    print(Dice.roll(d2).value)

    # roll seed test
    d3 = Dice.roll(d2, seed=5)
    d4 = Dice.roll(d3, seed=5)

    print(d3.value, d4.value)
    print(d3.value == d4.value)


if __name__ == "__main__":
    test()
