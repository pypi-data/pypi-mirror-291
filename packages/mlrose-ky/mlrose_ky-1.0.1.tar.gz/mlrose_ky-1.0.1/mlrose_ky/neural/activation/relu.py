"""Neural network activation functions."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

from mlrose_ky.decorators import short_name

import warnings
import numpy as np

warnings.filterwarnings("ignore")


@short_name("relu")
def relu(x, deriv=False):
    """ReLU activation function

    Parameters
    ----------
    x: np.ndarray
        Array containing input data.

    deriv: bool, default: False
        Whether to return the function or its derivative.
        Set True for derivative.

    Returns
    -------
    fx: np.ndarray
        Value of activation function at x
    """
    fx = np.copy(x)
    fx[np.where(fx < 0)] = 0

    if deriv:
        fx[np.where(fx > 0)] = 1

    return fx
