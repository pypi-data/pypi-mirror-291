"""Discrete Gene Mutator for Genetic Algorithms (GA)."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np
from typing import Any

from mlrose_ky.algorithms.mutators._mutator_base import _MutatorBase


class DiscreteGeneMutator(_MutatorBase):
    """
    A mutator class that performs discrete mutation on individual genes in a genetic algorithm.

    This class supports mutation where each gene in the chromosome can be discretely modified
    based on the mutation probability and the nature of the gene values.

    Attributes
    ----------
    optimization_problem : Any
        The optimization problem instance associated with the mutation operations.
    max_gene_value : int
        The maximum allowable value for any gene in the chromosome.

    Parameters
    ----------
    optimization_problem : Any
        An instance of an optimization problem that the mutator will operate on.
    """

    def __init__(self, optimization_problem: Any) -> None:
        super().__init__(optimization_problem)
        self.max_gene_value = optimization_problem.max_val

    def mutate(self, child: np.ndarray, mutation_probability: float) -> np.ndarray:
        """
        Apply discrete mutation to a chromosome based on a given mutation probability.

        The method supports two mutation modes: binary mutation (for binary genes) and discrete
        value mutation for genes that can take on multiple discrete values.

        Parameters
        ----------
        child : np.ndarray
            The chromosome of a child individual to be mutated.
        mutation_probability : float
            The probability of each gene being mutated.

        Returns
        -------
        np.ndarray
            The mutated chromosome.
        """
        random_thresholds = np.random.uniform(size=self.chromosome_length)
        mutation_indices = np.where(random_thresholds < mutation_probability)[0]

        if self.max_gene_value == 2:
            child[mutation_indices] = 1 - child[mutation_indices]
        else:
            for index in mutation_indices:
                possible_values = list(range(self.max_gene_value))
                possible_values.remove(child[index])
                child[index] = np.random.choice(possible_values)

        return child
