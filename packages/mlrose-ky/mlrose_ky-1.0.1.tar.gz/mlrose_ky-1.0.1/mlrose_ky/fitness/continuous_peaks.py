"""Class defining the Continuous Peaks fitness function for use with optimization algorithms."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np


class ContinuousPeaks:
    """
    Fitness function for Continuous Peaks optimization problem. Evaluates the fitness
    of an n-dimensional state vector `x`, given parameter T.

    Parameters
    ----------
    threshold_percentage : float, default=0.1
        Threshold parameter (T) for Continuous Peaks fitness function, expressed as a
        percentage of the state space dimension, n (i.e., `T = threshold_percentage * n`).

    Attributes
    ----------
    threshold_percentage : float
        The threshold percentage for the fitness function.
    problem_type : str
        Specifies problem type as 'discrete'.

    Examples
    --------
    >>> fitness = ContinuousPeaks(threshold_percentage=0.15)
    >>> state = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1])
    >>> fitness.evaluate(state)
    17.0

    Note
    ----
    The Continuous Peaks fitness function is suitable for use in bit-string (discrete-state
    with `max_val = 2`) optimization problems only.
    """

    def __init__(self, threshold_percentage: float = 0.1) -> None:
        self.threshold_percentage: float = threshold_percentage
        self.problem_type: str = "discrete"

        if not (0 <= self.threshold_percentage <= 1):
            raise ValueError(f"threshold_percentage must be between 0 and 1, got {self.threshold_percentage} instead.")

    def evaluate(self, state: np.ndarray) -> float:
        """
        Evaluate the fitness of a state vector.

        Parameters
        ----------
        state : np.ndarray
            State array for evaluation.

        Returns
        -------
        float
            Value of the fitness function.
        """
        num_elements = len(state)
        threshold = int(np.ceil(self.threshold_percentage * num_elements))

        max_zeros = self._max_run(0, state)
        max_ones = self._max_run(1, state)

        reward = num_elements if max_zeros > threshold and max_ones > threshold else 0

        fitness = float(max(max_zeros, max_ones) + reward)
        return fitness

    def get_problem_type(self) -> str:
        """
        Return the problem type.

        Returns
        -------
        str
            Specifies problem type as 'discrete'.
        """
        return self.problem_type

    @staticmethod
    def _max_run(value: int, vector: np.ndarray) -> int:
        """
        Determine the length of the maximum run of a given value in a vector.

        Parameters
        ----------
        value : int
            Value to count.
        vector : np.ndarray
            Vector of integers.

        Returns
        -------
        int
            Length of the maximum run of the given value.
        """
        # Create a boolean array where each element is True if it equals the given value
        is_value = np.array(vector == value)

        # If the value does not exist in the vector, return 0
        if not np.any(is_value):
            return 0

        # Calculate the differences between consecutive elements in the boolean array
        diffs = np.diff(is_value.astype(int))

        # Find the indices where the value starts and ends
        run_starts = np.where(diffs == 1)[0] + 1
        run_ends = np.where(diffs == -1)[0] + 1

        # If the run starts at the beginning of the vector, include the first index
        if is_value[0]:
            run_starts = np.insert(run_starts, 0, 0)

        # If the run ends at the end of the vector, include the last index
        if is_value[-1]:
            run_ends = np.append(run_ends, len(vector))

        # Ensure that run_ends has the same length as run_starts
        if len(run_starts) > len(run_ends):
            run_ends = np.append(run_ends, len(vector))

        # Calculate the lengths of the runs
        run_lengths = run_ends - run_starts

        # Return the maximum run length, or 0 if no runs are found
        return run_lengths.max() if run_lengths.size > 0 else 0
