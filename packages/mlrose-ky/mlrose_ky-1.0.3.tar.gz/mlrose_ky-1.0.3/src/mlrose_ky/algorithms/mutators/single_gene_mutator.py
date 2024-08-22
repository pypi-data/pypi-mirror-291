"""Single Gene (Change One) Mutator for Genetic Algorithms (GA)."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np
from typing import Any

from mlrose_ky.algorithms.mutators._mutator_base import _MutatorBase


class SingleGeneMutator(_MutatorBase):
    """
    A mutator class that performs the 'Change One' mutation strategy in a genetic algorithm.

    This mutator changes one randomly selected gene in the chromosome to a new value within the allowed range.

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
        Apply 'Change One' mutation operation to a given child chromosome based on a mutation probability.

        Randomly selects one gene and changes its value to a random value within the permissible range.

        Parameters
        ----------
        child : np.ndarray
            The chromosome of a child individual to be mutated.
        mutation_probability : float
            The probability of the child undergoing mutation.

        Returns
        -------
        np.ndarray
            The mutated chromosome.

        Raises
        ------
        ValueError
            If the mutation_probability is not within the range [0, 1].
        """
        if not (0 <= mutation_probability <= 1):
            raise ValueError(f"Mutation probability must be between 0 and 1, got {mutation_probability}")

        if np.random.rand() < mutation_probability:
            mutation_index = np.random.randint(len(child))
            child[mutation_index] = np.random.randint(self.max_gene_value)

        return child
