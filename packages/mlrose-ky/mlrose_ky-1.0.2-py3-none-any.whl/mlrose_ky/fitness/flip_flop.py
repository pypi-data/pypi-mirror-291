"""Class defining the Flip Flop fitness function for use with optimization algorithms."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np


class FlipFlop:
    """Fitness function for Flip Flop optimization problem.

    Evaluates the fitness of a state vector :math:`x` as the total number of pairs of consecutive
    elements of :math:`x`, (:math:`x_{i}` and :math:`x_{i+1}`) where :math:`x_{i} \\neq x_{i+1}`.

    Examples
    --------
    >>> fitness = FlipFlop()
    >>> state_vector = np.array([0, 1, 0, 1, 1, 1, 1])
    >>> fitness.evaluate(state_vector)
    3.0

    Note
    ----
    The Flip Flop fitness function is suitable for use in discrete-state
    optimization problems *only*.
    """

    def __init__(self):
        """Initialize the Flip Flop fitness function."""
        self.problem_type: str = "discrete"

    @staticmethod
    def evaluate(state_vector: np.ndarray) -> float:
        """Evaluate the fitness of a state vector.

        Parameters
        ----------
        state_vector : np.ndarray
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

        differences = np.diff(state_vector) != 0
        fitness = float(np.sum(differences))
        return fitness

    @staticmethod
    def evaluate_many(state_matrix: np.ndarray) -> np.ndarray:
        """Evaluate the fitness of an ndarray of state vectors.

        Parameters
        ----------
        state_matrix : np.ndarray
            States array for evaluation.

        Returns
        -------
        np.ndarray
            Array of fitness values.

        Raises
        ------
        TypeError
            If `state_matrix` is not an instance of `np.ndarray`.
        """
        if not isinstance(state_matrix, np.ndarray):
            raise TypeError(f"Expected state_matrix to be np.ndarray, got {type(state_matrix).__name__} instead.")

        differences = np.diff(state_matrix, axis=1) != 0
        fitness_values = np.sum(differences, axis=1)
        return fitness_values

    def get_problem_type(self) -> str:
        """Return the problem type.

        Returns
        -------
        str
            Specifies problem type as 'discrete'.
        """
        return self.problem_type
