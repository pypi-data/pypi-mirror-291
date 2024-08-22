"""Class defining a Continuous Peaks optimization problem generator."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np

from src.mlrose_ky import DiscreteOpt, ContinuousPeaks


class ContinuousPeaksGenerator:
    """A class to generate Continuous Peaks optimization problems."""

    @staticmethod
    def generate(seed: int, size: int = 20, threshold_percentage: float = 0.1) -> DiscreteOpt:
        """
        Generate a Continuous Peaks optimization problem instance.

        Parameters
        ----------
        seed : int
            Seed for the random number generator.
        size : int, optional, default=20
            The size of the optimization problem.
        threshold_percentage : float, optional, default=0.1
            The threshold percentage for the Continuous Peaks fitness function.

        Returns
        -------
        problem : Any
            An instance of the DiscreteOpt class representing the optimization problem.

        Raises
        ------
        ValueError
            If the `size` is not a positive integer or if `threshold_percentage` is not between 0 and 1.
        """
        if not isinstance(size, int) or size <= 0:
            raise ValueError(f"Size must be a positive integer. Got {size}")
        if not isinstance(threshold_percentage, float):
            raise ValueError(f"Threshold percentage must be a float. Got {type(threshold_percentage).__name__}")
        if not (0 <= threshold_percentage <= 1):
            raise ValueError(f"Threshold percentage must be between 0 and 1. Got {threshold_percentage}")

        np.random.seed(seed)

        fitness = ContinuousPeaks(threshold_percentage=threshold_percentage)
        problem = DiscreteOpt(length=size, fitness_fn=fitness)

        return problem
