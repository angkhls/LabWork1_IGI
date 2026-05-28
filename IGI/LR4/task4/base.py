"""
Lab Work #4 - Task 4: Geometric Figure Base Classes

"""

from abc import ABC, abstractmethod


class FigureColor:

    def __init__(self, color: str = 'blue'):

        self.color = color

    @property
    def color(self):
        """Return the figure's current color as a lowercase string."""
        return self._color

    @color.setter
    def color(self, value: str):
        """
        Set the figure color after validation.
.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Color must be a non-empty string.")
        self._color = value.strip().lower()


class GeometricFigure(ABC):
    """
    Abstract base class for all geometric figures.

    """

    figure_name: str = "GeometricFigure"

    @abstractmethod
    def area(self):
        """
        Calculate and return the area of the figure.

        Returns:
            float: Area value.
        """
        pass

    @classmethod
    def get_figure_name(cls):
        """
        Class method: return the name of this figure type.

        """
        return cls.figure_name
