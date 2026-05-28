"""
Lab Work #4 - Task 3
"""

import math
import statistics


class SeriesCalculator:
    """
    Calculator for the Taylor series expansion of ln(1-x).

    """

    FORMULA_STR = "ln(1-x) = -x - x²/2 - x³/3 - ..."

    def __init__(self, x: float, n_terms: int):
        """
        Initialize the calculator and compute all partial sums.

        """
        if abs(x) >= 1:
            raise ValueError(f"x must satisfy |x| < 1, got x={x}")
        if n_terms < 1:
            raise ValueError("n_terms must be >= 1")
        self.x = x
        self.n_terms = n_terms
        self._series_values: list[float] = []
        self._compute()

    def _compute(self):
        """
        Internal method: accumulate partial sums and store each in _series_values.
        The n-th term is  -(x^n / n).
        """
        total = 0.0
        for n in range(1, self.n_terms + 1):
            total += -(self.x ** n) / n
            self._series_values.append(total)

    @property
    def series_values(self):
        """Return the list of partial sums computed by the series."""
        return self._series_values

    @property
    def final_value(self):
        """Return the final (n-th partial sum) approximation of ln(1-x)."""
        return self._series_values[-1]

    @property
    def math_value(self):
        """Return the exact value of ln(1-x) using math.log."""
        return math.log(1 - self.x)

    @property
    def epsilon(self):
        """Return the absolute error between the series approximation and the exact value."""
        return abs(self.final_value - self.math_value)

    def get_stats(self):
        """
        Compute descriptive statistics for the sequence of partial sums.

        Returns:
            dict with keys: mean, median, mode, variance, stdev.
            'mode' is 'No unique mode' if all values differ after rounding to 6 decimals.
        """
        rounded = [round(v, 6) for v in self._series_values]
        try:
            mode_val = statistics.mode(rounded)
        except statistics.StatisticsError:
            mode_val = "No unique mode"

        return {
            "mean":     statistics.mean(self._series_values),
            "median":   statistics.median(self._series_values),
            "mode":     mode_val,
            "variance": statistics.variance(self._series_values),
            "stdev":    statistics.stdev(self._series_values),
        }
