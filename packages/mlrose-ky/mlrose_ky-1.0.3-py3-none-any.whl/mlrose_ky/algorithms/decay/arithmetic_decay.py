"""Class for defining an arithmetic decay schedule for Simulated Annealing (SA)."""

# Authors: Genevieve Hayes (modified by Andrew Rollings, Kyle Nakamura)
# License: BSD 3-clause


class ArithmeticDecay:
    """
    Schedule for arithmetically decaying the temperature parameter T in a
    simulated annealing process, calculated using the formula:

    .. math::

        T(t) = \\max(T_{0} - rt, T_{min})

    where :math:`T_{0}` is the initial temperature at time `t = 0`, `r` is the decay rate, and :math:`T_{min}`
    is the minimum temperature.

    Parameters
    ----------
    initial_temperature : float
        Initial value of the temperature parameter T. Must be greater than 0.
    decay_rate : float
        Temperature decay parameter. Must be a positive value and less than or equal to 1.
    minimum_temperature : float
        Minimum allowable value of the temperature parameter. Must be positive and less than `initial_temperature`.

    Attributes
    ----------
    initial_temperature : float
        Stores the initial temperature.
    decay_rate : float
        Stores the rate of temperature decay.
    minimum_temperature : float
        Stores the minimum temperature.

    Examples
    --------
    >>> schedule = ArithmeticDecay(initial_temperature=10, decay_rate=0.95, minimum_temperature=1)
    >>> schedule.evaluate(5)
    5.25
    """

    def __init__(self, initial_temperature: float = 1.0, decay_rate: float = 0.0001, minimum_temperature: float = 0.001) -> None:
        self.initial_temperature: float = initial_temperature
        self.decay_rate: float = decay_rate
        self.minimum_temperature: float = minimum_temperature

        if self.initial_temperature <= 0:
            raise ValueError("Initial temperature must be greater than 0.")
        if not (0 < self.decay_rate <= 1):
            raise ValueError("Decay rate must be greater than 0 and less than or equal to 1.")
        if not (0 < self.minimum_temperature < self.initial_temperature):
            raise ValueError("Minimum temperature must be greater than 0 and less than initial temperature.")

    def __str__(self) -> str:
        return (
            f"ArithmeticDecay(initial_temperature={self.initial_temperature}, "
            f"decay_rate={self.decay_rate}, "
            f"minimum_temperature={self.minimum_temperature})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ArithmeticDecay):
            return False
        return (
            self.initial_temperature == other.initial_temperature
            and self.decay_rate == other.decay_rate
            and self.minimum_temperature == other.minimum_temperature
        )

    def evaluate(self, time: int) -> float:
        """
        Calculate and return the temperature parameter at the given time.

        Parameters
        ----------
        time : int
            The time at which to evaluate the temperature parameter.

        Returns
        -------
        float
            The temperature parameter at the given time, respecting the minimum temperature.
        """
        temperature = max(self.initial_temperature - (self.decay_rate * time), self.minimum_temperature)
        return temperature

    def get_info(self, time: int = None, prefix: str = "") -> dict:
        """
        Generate a dictionary containing the decay schedule's settings and optionally its current value.

        Parameters
        ----------
        time : int, optional
            The time at which to evaluate the current temperature value.
            If provided, the current value is included in the returned dictionary.
        prefix : str, optional
            A prefix to prepend to each key in the dictionary, useful for integrating this info into larger structured data.

        Returns
        -------
        dict
            A dictionary with keys reflecting the decay schedule's parameters and optionally the current temperature.
        """
        info_prefix = f"{prefix}schedule_" if prefix else "schedule_"

        info = {
            f"{info_prefix}type": "arithmetic",
            f"{info_prefix}initial_temperature": self.initial_temperature,
            f"{info_prefix}decay_rate": self.decay_rate,
            f"{info_prefix}minimum_temperature": self.minimum_temperature,
        }

        if time is not None:
            info[f"{info_prefix}current_value"] = self.evaluate(time)

        return info
