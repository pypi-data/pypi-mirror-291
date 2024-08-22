"""Single Shift (Shift One) Mutator for Genetic Algorithms (GA)."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np
from typing import Any

from src.mlrose_ky.algorithms.mutators._mutator_base import _MutatorBase


class SingleShiftMutator(_MutatorBase):
    """
    A mutator class that implements the 'Shift One' mutation strategy in a genetic algorithm.

    This mutator adjusts a single gene in the chromosome either up or down by one,
    wrapping around the maximum value constraint to ensure all values remain valid.

    Attributes
    ----------
    optimization_problem : Any
        The optimization problem instance associated with the mutation operations.
    max_gene_value : int
        The maximum allowable value for any gene in the chromosome, used to enforce wrap-around.

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
        Apply a 'Shift One' mutation to a randomly selected gene in the chromosome if the mutation
        probability condition is met. The selected gene's value is incremented or decremented by one,
        with wrap-around handling to stay within permissible value ranges.

        Parameters
        ----------
        child : np.ndarray
            The chromosome of a child individual to be mutated.
        mutation_probability : float
            The probability of the child undergoing a mutation.

        Returns
        -------
        np.ndarray
            The mutated chromosome.
        """
        if np.random.rand() < mutation_probability:
            mutation_index = np.random.randint(len(child))
            shift_direction = 1 if np.random.randint(2) == 0 else -1
            new_value = (child[mutation_index] + shift_direction) % self.max_gene_value
            child[mutation_index] = new_value

        return child
