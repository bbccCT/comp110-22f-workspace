"""Utility class for numerical operations."""

from __future__ import annotations

from typing import Union

__author__ = "730605992"


class Simpy:
    """A simple class recreating some of the simpler functionalities of NumPy."""
    values: list[float]

    def __init__(self, values: list[float]):
        """Assign given values to object's list."""
        self.values = values

    def __repr__(self) -> str:
        """Return a string representation of a constructor for this object."""
        return f"Simpy({self.values})"

    def fill(self, filling: float, length: int) -> None:
        """Reset and fill this object with a certain float for a certain number of items."""
        self.values = []
        for i in range(length):
            self.values.append(filling)

    def arange(self, start: float, stop: float, step: float = 1.0) -> None:
        """Fill (additive) this object with a sequence of numbers between given starting and stopping floats [x,y) with an optional float for steps between each iteration."""
        assert step != 0.0
        i: float = start
        if step > 0:
            while i < stop:
                self.values.append(i)
                i += step
        else:
            while i > stop:
                self.values.append(i)
                i += step

    def sum(self) -> float:
        """Return a float for all floats in values added together."""
        return sum(self.values)

    def __add__(self, rhs: Union[float, Simpy]) -> Simpy:
        """Overrides the + operator for floats and other Simpy objects."""
        result: Simpy = Simpy([])
        if isinstance(rhs, Simpy):
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                result.values.append(self.values[i] + rhs.values[i])
        elif isinstance(rhs, float):
            for i in range(len(self.values)):
                result.values.append(self.values[i] + rhs)
        return result

    def __pow__(self, rhs: Union[float, Simpy]) -> Simpy:
        """Overrides the ** operator for floats and other Simpy objects."""
        result: Simpy = Simpy([])
        if isinstance(rhs, Simpy):
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                result.values.append(pow(self.values[i], rhs.values[i]))
        elif isinstance(rhs, float):
            for i in range(len(self.values)):
                result.values.append(pow(self.values[i], rhs))
        return result

    def __eq__(self, rhs: Union[float, Simpy]) -> list[bool]:
        """Overrides the == operator and returns a mask as a list of bools."""
        result: list[bool] = []
        if isinstance(rhs, Simpy):
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                if self.values[i] == rhs.values[i]:
                    result.append(True)
                else:
                    result.append(False)
        elif isinstance(rhs, float):
            for i in range(len(self.values)):
                if self.values[i] == rhs:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def __gt__(self, rhs: Union[float, Simpy]) -> list[bool]:
        """Overrides the > operator and returns a mask as a list of bools."""
        result: list[bool] = []
        if isinstance(rhs, Simpy):
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                if self.values[i] > rhs.values[i]:
                    result.append(True)
                else:
                    result.append(False)
        elif isinstance(rhs, float):
            for i in range(len(self.values)):
                if self.values[i] > rhs:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def __getitem__(self, rhs: Union[int, list[bool]]) -> Union[float, Simpy]:
        """Subscription notation."""
        if isinstance(rhs, int):
            return self.values[rhs]
        elif isinstance(rhs, list):
            if isinstance(rhs[0], bool):
                result: Simpy = Simpy([])
                for i in range(len(self.values)):
                    if rhs[i]:
                        result.values.append(self.values[i])
                return result