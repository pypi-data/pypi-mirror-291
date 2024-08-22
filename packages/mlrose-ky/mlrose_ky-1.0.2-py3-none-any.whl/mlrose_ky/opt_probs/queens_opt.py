"""Classes for defining optimization problem objects."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np

from src.mlrose_ky.algorithms.crossovers import UniformCrossover
from src.mlrose_ky.algorithms.mutators import SingleGeneMutator
from src.mlrose_ky.fitness.queens import Queens
from src.mlrose_ky.opt_probs.discrete_opt import DiscreteOpt


class QueensOpt(DiscreteOpt):
    def __init__(self, length=None, fitness_fn=None, maximize=False, crossover=None, mutator=None):

        if (fitness_fn is None) and (length is None):
            raise Exception("fitness_fn or length must be specified.")

        if length is None:
            length = len(fitness_fn.weights)

        self.length = length

        if fitness_fn is None:
            fitness_fn = Queens(maximize=maximize)

        self.stop_fitness = Queens.get_max_size(length) if maximize else 0

        self.max_val = length
        crossover = UniformCrossover(self) if crossover is None else crossover
        mutator = SingleGeneMutator(self) if mutator is None else mutator
        super().__init__(length, fitness_fn, maximize, length, crossover, mutator)

        state = np.random.randint(self.length, size=self.length)
        np.random.shuffle(state)
        self.set_state(state)

    def can_stop(self):
        return int(self.get_fitness()) == self.stop_fitness
