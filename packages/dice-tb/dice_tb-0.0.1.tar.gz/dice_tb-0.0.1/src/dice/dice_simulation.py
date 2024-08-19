# imports random module for random number generation for random dice values
import random

# imports dataclass which is used to create datatypes for dice and state
from dataclasses import dataclass

# import plt for plotting the histogram and the plot overlay
import matplotlib.pyplot as plt

# import numpy which is used for plotting
import numpy as np

# typing annotations for function
from typing import Callable
from typing import Any
from typing import Union

import dice as _dice


_args  = Union[Any, None]
_state = Any 


@dataclass
class MonteCarloSimulation:
    other_args                  : _args
    setup_before_all_simulations: Callable[_args, _state]
    simulation_loop_body        : Callable[[_state, _args], _state] 
    """
        before_each_simulation      : Callable[[_state, _args], _state] 
        simulate                    : Callable[[_state, _args], _args]
        after_each_simulation       : Callable[[_state, _args], _state]
    """
    display                     : Callable[_state, _args]


    def __post_init__(self):
        pass


    def run_simulation(self, number_of_simulations: int = 1000):
        if type(number_of_simulations) == int:

            if 0 < number_of_simulations:
                state = self.setup_before_all_simulations()       # setup before all simulations

                for i in range(number_of_simulations):
                    state = self.simulation_loop_body(state)

                self.display(state)

            else:
                raise ValueError()

        else:
            raise TypeError()


def monte_carlo(number_of_simulations: int):
    # args 
    # setup_before_all_simulations(args) -> State:
    # simulation_loop_body(state, args) -> State:
    #     before_each_simulation(state, args) -> State:
    #     simulate(state, args) -> args:
    #     after_each_simulation(state, args) -> State:
    #         calculate(args) -> args
    #         aggregate(args) -> state
    # display(state)

    if type(number_of_simulations) == int:

        if 0 < number_of_simulations:
            state = setup_before_all_simulations()       # setup before all simulations

            for i in range(number_of_simulations):
                state = simulation_loop_body(state)

            display(state)

        else:
            raise ValueError()

    else:
        raise TypeError()


@dataclass
class State:
    # d1 : Dice
    # d2 : Dice
    ds : list
    # br : int
    # rls: int

    def __post_init__(self):
        if type(self.ds) == list: #type(self.d1) == Dice and type(self.d2) == Dice and  and type(self.br) == int and type(self.rls):
            pass
            #if 0 <= self.br: 
            #    if 0 <= self.rls:
            #        pass

            #    else:
            #        ValueError()
            
            #else:
            #    ValueError()

        else:
            raise TypeError()


def setup_before_all_simulations() -> State:
    #d1  = Dice(sides=6)
    #d2  = Dice(sides=6)
    ds  = []
    #br  = 100
    #rls = 0

    return State(ds) #d1, d2, ds, br, rls)


def simulation_loop_body(state: State) -> State:
    state = before_each_simulation(state)
    br    = simulate(state)
    state = after_each_simulation(state, br)

    return state


def before_each_simulation(state: State) -> State:
    return state


def simulate(state: State, br=100, rls=0) -> int: 
    if rls <= 100 and 0 < br :
        d = _dice.Dice(6)
        d1, d2 = _dice.Dice.roll(d), _dice.Dice.roll(d)

        # seeding: d1, d2 = _dice.Dice.roll(d, 5), _dice.Dice.roll(d, 5)

        if d1.value + d2.value == 7 or d1.value + d2.value == 11 or d1.value == d2.value:
            br = br + 2

            return simulate(state, br, rls + 1)

        else:
            br = br - 1

            return simulate(state, br, rls + 1)

    else:
        return br


def after_each_simulation(state: State, br: int) -> State: 

    def calculate(br: int) -> int:
        return br

    def aggregate(br: int) -> State:
        ds = state.ds + [calculate(br)]

        return State(ds)
 
    return aggregate(br)


def display(state: State):
    if type(state) == State:
        
        data = np.array(state.ds)

        if len(state.ds) == 0:
            print("No Chart")

        else:
            # Standard deviation of list 
            # Using sum() + list comprehension 
            mean     = sum(state.ds) / len(state.ds) 
            variance = sum([((x - mean) ** 2) for x in state.ds]) / len(state.ds) 
            res      = variance ** 0.5

            if np.unique(data).size == 1:
                d                 = data[0]
                left_of_first_bin = d - 1 
                right_of_last_bin = d + 1 

                plt.hist(data, range=(0, right_of_last_bin+d))

            else:
                d                 = np.diff(np.unique(data)).min()
                left_of_first_bin = data.min() - float(d)/2
                right_of_last_bin = data.max() + float(d)/2
                plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d , d))
                
            plt.text(1, 0, 'mean = ' + str(mean) + ', var = ' + str(variance) + ', std = ' + str(res), fontsize = 10)
            plt.xlabel("2 Dice Sum", fontsize = 15)
            plt.ylabel("Frequency", fontsize = 15)
            
            """i=-30                      # intercept
            s= 30                      # slope
            x=np.linspace(2, 7, 50)    # from 1 to 10, by 50
            plt.plot(x, s*x + i)       # abline
            
            j= 390                      # intercept
            t=-30                       # slope
            x=np.linspace(7, 12, 50)    # from 7 to 12, by 50
            plt.plot(x, t*x + j)        # abline"""
        
            plt.show()

    else:
        raise TypeError()


if __name__ == "__main__":
    #monte_carlo_simulation = MonteCarloSimulation(None, setup_before_all_simulations, simulation_loop_body, display)
    #monte_carlo_simulation.run_simulation()
    monte_carlo(1000)
