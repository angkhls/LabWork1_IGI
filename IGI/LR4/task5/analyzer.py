"""
Lab Work #4 - Task 5: NumPy Matrix Analyzer
"""

import numpy as np


class MatrixAnalyzer:
    """
    Generates a random integer matrix and exposes NumPy-based analysis methods.

    Variant 29 tasks:
      a) Compute the sum of elements strictly below the main diagonal.
      b) Compare NumPy std vs manually computed std for the main diagonal.
    """

    RAND_LOW:  int = -50
    RAND_HIGH: int =  50

    def __init__(self, n: int, m: int, seed: int = None):
        """
        Initialize and generate the n×m random integer matrix.

        """
        if n < 2 or m < 2:
            raise ValueError("Matrix dimensions must be at least 2×2.")
        self._n, self._m = n, m
        rng = np.random.default_rng(seed)
        self._matrix = rng.integers(self.RAND_LOW, self.RAND_HIGH + 1, size=(n, m))

    @property
    def matrix(self):
        """Return a copy of the internal matrix to prevent external mutation."""
        return self._matrix.copy()

    def sum_below_main_diagonal(self) -> int:
        """
        Variant 29a: Return the sum of all elements strictly below the main diagonal.

        """
        below_mask = np.tril(np.ones_like(self._matrix, dtype=bool), k=-1)
        return int(np.sum(self._matrix[below_mask]))

    def std_diagonal_comparison(self) -> tuple:
        """
        Variant 29b: Compute the standard deviation of main-diagonal elements two ways.

        Method 1 – NumPy:    np.std(diag)
        Method 2 – Manual:   sqrt( mean( (xi - mean)² ) )

        """
        diag = np.diag(self._matrix).astype(float)
        std_np     = round(float(np.std(diag)), 2)
        mean_val   = np.mean(diag)
        std_manual = round(float(np.sqrt(np.mean((diag - mean_val) ** 2))), 2)
        return std_np, std_manual

    def get_main_stats(self) -> dict:
        """
        Compute basic descriptive statistics for all matrix elements.

        Returns:
            dict with keys: mean, median, std.
        """
        return {
            "mean":   float(np.mean(self._matrix)),
            "median": float(np.median(self._matrix)),
            "std":    float(np.std(self._matrix)),
        }

    def __str__(self) -> str:
        """Magic method: return the matrix as a formatted NumPy string."""
        return str(self._matrix)
