"""Neural network activation functions."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause
from src.mlrose_ky.decorators import short_name

import numpy as np

import warnings

warnings.filterwarnings("ignore")


@short_name("softmax")
def softmax(x):
    """Softmax activation function

    Parameters
    ----------
    x: np.ndarray
        Array containing input data.

    Returns
    -------
    fx: np.ndarray
        Value of activation function at x
    """
    max_prob = np.max(x, axis=1).reshape((-1, 1))
    fx = np.exp(x - max_prob)
    sum_prob = np.sum(fx, axis=1).reshape((-1, 1))
    fx = np.divide(fx, sum_prob)

    return fx
