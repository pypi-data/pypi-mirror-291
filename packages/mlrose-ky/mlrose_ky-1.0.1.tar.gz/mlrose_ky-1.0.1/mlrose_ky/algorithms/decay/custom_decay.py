"""Class for defining a custom decay schedule for Simulated Annealing (SA)."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause

from typing import Callable


class CustomDecay:
    """
    Class for generating a customizable temperature schedule for simulated annealing.

    This class allows the user to define a custom decay function that calculates the temperature
    based on the time and potentially other parameters.

    Parameters
    ----------
    decay_function : Callable[..., float]
        A function with the signature `decay_function(t: int, **kwargs)` that calculates the temperature at time t.
    **kwargs : dict
        Additional keyword arguments to be passed to the decay function.

    Examples
    -------
    >>> def custom_decay_function(time: int, offset: int) -> float: return time + offset
    >>> kwargs = {'offset': 10}
    >>> schedule = CustomDecay(custom_decay_function, **kwargs)
    >>> schedule.evaluate(5)
    15
    """

    def __init__(self, decay_function: Callable[..., float], **kwargs) -> None:
        self.decay_function: Callable[..., float] = decay_function
        self.kwargs: dict = kwargs

    def __str__(self) -> str:
        return f"CustomDecay(function={self.decay_function.__name__}, parameters={self.kwargs})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomDecay):
            return False
        return self.decay_function == other.decay_function and self.kwargs == other.kwargs

    def evaluate(self, time: int) -> float:
        """
        Evaluate the temperature parameter at the specified time using the custom decay function.

        Parameters
        ----------
        time : int
            The time at which to evaluate the temperature parameter.

        Returns
        -------
        float
            The calculated temperature at the specified time.
        """
        return self.decay_function(time, **self.kwargs)

    def get_info(self, time: int | None = None, prefix: str = "") -> dict:
        """
        Retrieve a dictionary containing the configuration of the decay schedule and optionally the current value.

        Parameters
        ----------
        time : int | None, optional
            If provided, include the current temperature value at the given time.
        prefix : str, optional
            A prefix to append to each dictionary key, enhancing integration with other data structures.

        Returns
        -------
        dict
            A dictionary detailing the decay schedule's settings and optionally the current temperature.
        """
        info_prefix = f"{prefix}schedule_" if prefix else "schedule_"

        info = {
            f"{info_prefix}type": "custom",
            f"{info_prefix}function": self.decay_function.__name__,
            **{f"{info_prefix}param_{key}": value for key, value in self.kwargs.items()},
        }

        if time is not None:
            info[f"{info_prefix}current_value"] = self.evaluate(time)

        return info
