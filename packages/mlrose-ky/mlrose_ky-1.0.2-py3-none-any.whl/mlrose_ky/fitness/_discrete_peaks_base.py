"""Class defining the Discrete Peaks base fitness function for use with the Four Peaks, Six Peaks, and Custom fitness functions."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

import numpy as np


class _DiscretePeaksBase:
    """Base class for Discrete Peaks fitness functions.

    This class provides methods to determine the number of leading or trailing
    specific integer values within a vector.
    """

    @staticmethod
    def count_leading_values(value: int, vector: np.ndarray) -> int:
        """Determine the number of leading occurrences of `value` in `vector`.

        Parameters
        ----------
        value : int
            The integer value to count at the beginning of the vector.
        vector : np.ndarray
            A vector of integers.

        Returns
        -------
        int
            Number of leading occurrences of `value` in `vector`.

        Raises
        ------
        TypeError
            If `vector` is not an instance of `np.ndarray`.
        """
        if not isinstance(vector, np.ndarray):
            raise TypeError(f"Expected vector to be np.ndarray, got {type(vector).__name__} instead.")

        # Use NumPy's cumulative sum to find leading values
        leading_mask = np.cumsum(vector != value) == 0
        return np.sum(leading_mask)

    @staticmethod
    def count_trailing_values(value: int, vector: np.ndarray) -> int:
        """Determine the number of trailing occurrences of `value` in `vector`.

        Parameters
        ----------
        value : int
            The integer value to count at the end of the vector.
        vector : np.ndarray
            A vector of integers.

        Returns
        -------
        int
            Number of trailing occurrences of `value` in `vector`.

        Raises
        ------
        TypeError
            If `vector` is not an instance of `np.ndarray`.
        """
        if not isinstance(vector, np.ndarray):
            raise TypeError(f"Expected vector to be np.ndarray, got {type(vector).__name__} instead.")

        # Use NumPy's cumulative sum to find trailing values
        trailing_mask = np.cumsum(vector[::-1] != value) == 0
        return np.sum(trailing_mask)
