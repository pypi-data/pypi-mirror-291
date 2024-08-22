"""Class defining a Six Peaks optimization problem generator."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np

from src.mlrose_ky import DiscreteOpt, SixPeaks


class SixPeaksGenerator:
    """A class to generate Six Peaks optimization problem instances."""

    @staticmethod
    def generate(seed: int, size: int = 20, threshold_percentage: float = 0.1) -> DiscreteOpt:
        """
        Generate a Six Peaks optimization problem with a given seed, size, and threshold percentage.

        Parameters
        ----------
        seed : int
            The seed for the random number generator.
        size : int, optional
            The size of the problem (default is 20).
        threshold_percentage : float, optional
            The threshold percentage for the Six Peaks problem (default is 0.1).

        Returns
        -------
        DiscreteOpt
            An instance of DiscreteOpt configured with the specified parameters.

        Raises
        ------
        ValueError
            If the size is not a positive integer or if the threshold_percentage is not between 0 and 1.
        """
        if size <= 0:
            raise ValueError(f"Size must be a positive integer. Got {size}.")
        if not (0 <= threshold_percentage <= 1):
            raise ValueError(f"Threshold percentage must be between 0 and 1. Got {threshold_percentage}.")

        np.random.seed(seed)

        fitness = SixPeaks(threshold_percentage=threshold_percentage)
        problem = DiscreteOpt(length=size, fitness_fn=fitness)

        return problem
