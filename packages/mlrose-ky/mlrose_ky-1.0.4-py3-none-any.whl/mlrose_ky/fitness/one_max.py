"""Class defining the One Max fitness function for use with optimization algorithms."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np


class OneMax:
    """Fitness function for One Max optimization problem.

    Evaluates the fitness of an n-dimensional state vector `x` as:

    .. math::

        Fitness(x) = \\sum_{i = 0}^{n-1}x_{i}

    Examples
    -------
    >>> fitness = OneMax()
    >>> state = np.array([0, 1, 0, 1, 1, 1, 1])
    >>> fitness.evaluate(state)
    5.0

    Note
    -----
    The One Max fitness function is suitable for use in either discrete or continuous-state optimization problems.
    """

    def __init__(self) -> None:
        self.problem_type: str = "either"

    @staticmethod
    def evaluate(state_vector: np.ndarray) -> float:
        """Evaluate the fitness of a state vector.

        Parameters
        ----------
        state_vector: np.ndarray
            State array for evaluation.

        Returns
        -------
        float
            Value of fitness function.

        Raises
        ------
        TypeError
            If `state_vector` is not an instance of `np.ndarray`.
        """
        if not isinstance(state_vector, np.ndarray):
            raise TypeError(f"Expected state_vector to be np.ndarray, got {type(state_vector).__name__} instead.")

        return float(np.sum(state_vector))

    def get_problem_type(self) -> str:
        """Return the problem type.

        Returns
        -------
        str
            Specifies problem type as 'either'.
        """
        return self.problem_type
