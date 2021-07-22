# Base imports
from typing import Union


Number = Union[int, float]


class BoundedNumber:
    def __init__(self, value: Number, _min: Number = 1, _max: Number = 10):
        self._min = _min
        self._max = _max
        self.set(value)

    @property
    def min(self) -> Number:
        return self._min

    @property
    def max(self) -> Number:
        return self._max

    @min.setter
    def min(self, new_min: Number) -> None:
        if isinstance(new_min, (str, int, float)):
            try:
                self._min = float(new_min)
            except ValueError:
                raise ValueError('Please enter a valid numeric string.')
        else:
            raise TypeError('Please enter a valid minimum value.')

    @max.setter
    def max(self, new_max: Number) -> None:
        if isinstance(new_max, (str, int, float)):
            try:
                self._max = float(new_max)
            except ValueError:
                raise ValueError('Please enter a valid numeric string.')
        else:
            raise TypeError('Please enter a valid maximum value.')

    def set(self, new_value: Number) -> None:


        
        self.value = max(self._min, min(self._max, new_value))
