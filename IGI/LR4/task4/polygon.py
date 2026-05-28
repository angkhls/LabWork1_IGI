"""
Lab Work #4 - Task 4: Regular Polygon (Variant 29)
Implements a regular n-gon with drawing and area calculation.
Version: 1.0
Developer: Student, Variant 29
"""

import math
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .base import GeometricFigure, FigureColor


class RegularPolygon(GeometricFigure, FigureColor):
    """
    polygon with n equal sides

    """

    figure_name = "Regular Polygon"
    count = 0

    def __init__(self, n: int, side: float, color: str = 'blue', label: str = ''):
        """
        Initialize a regular polygon.

        """
        GeometricFigure.__init__(self)
        FigureColor.__init__(self, color)
        self.n    = n
        self.side = side
        self._label = label
        RegularPolygon.count += 1

    @property
    def n(self):
        """Return the number of sides of the polygon."""
        return self._n

    @n.setter
    def n(self, value: int):
        """
        Set the number of sides with validation.

        """
        if value < 3:
            raise ValueError("A polygon must have at least 3 sides.")
        self._n = value

    @property
    def side(self):
        """Return the side length of the polygon."""
        return self._side

    @side.setter
    def side(self, value: float):
        """
        Set the side length with validation.

        """
        if value <= 0:
            raise ValueError("Side length must be a positive number.")
        self._side = value

    def area(self):
        """
        Calculate the area of the regular polygon using the standard formula.

            A = (n * a²) / (4 * tan(π/n))

        """
        return (self._n * self._side ** 2) / (4 * math.tan(math.pi / self._n))

    @property
    def perimeter(self):
        """Return the perimeter of the polygon (n × side)."""
        return self._n * self._side

    def __str__(self):
        """Magic method: human-readable description of the polygon."""
        return (
            f"{self.figure_name}: n={self._n} sides, side={self._side}, "
            f"color={self._color}, area={self.area():.4f}, perimeter={self.perimeter:.4f}"
        )

    def draw_and_save(self, path: str = "task4/polygon.png"):
        """
        Draw the regular polygon, fill it with the chosen color, add a label,
        and save the image to a PNG file.

        """
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)

        R = self._side / (2 * math.sin(math.pi / self._n))
        vertices = [
            (R * math.cos(math.pi / 2 + 2 * math.pi * k / self._n),
             R * math.sin(math.pi / 2 + 2 * math.pi * k / self._n))
            for k in range(self._n)
        ]

        fig, ax = plt.subplots(figsize=(6, 6))
        poly_patch = plt.Polygon(vertices, facecolor=self._color,
                                 edgecolor='black', linewidth=2)
        ax.add_patch(poly_patch)


        label_text = self._label if self._label else f"{self._n}-gon"
        ax.text(0, 0, label_text, ha='center', va='center',
                fontsize=12, fontweight='bold')

        ax.set_aspect('equal')
        margin = R * 0.3
        ax.set_xlim(-R - margin, R + margin)
        ax.set_ylim(-R - margin, R + margin)
        ax.set_title(f"{self.figure_name} (n={self._n}, a={self._side}, color={self._color})")
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=100)
        plt.close()
        return path
