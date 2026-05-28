"""
Lab Work #4 - Task 5: NumPy Feature Demonstrations
Shows NumPy array creation, indexing, and universal functions.
Version: 1.0
Developer: Student, Variant 29
"""

import numpy as np


def demo_numpy_features(analyzer) -> None:
    """
    Demonstrate core NumPy capabilities using the provided MatrixAnalyzer.

    Covers:
      - Array creation: zeros, linspace, from existing data
      - Indexing: element access, row/column slices
      - Universal (element-wise) functions: abs, max

    Args:
        analyzer (MatrixAnalyzer): An initialized analyzer whose matrix is used.
    """
    print("\n--- NumPy Feature Demo ---")

    print("np.zeros((2,2)):\n", np.zeros((2, 2)))
    print("np.ones((2,3)):\n", np.ones((2, 3)))
    print("np.linspace(0, 10, 5):", np.linspace(0, 10, 5))
    print("np.arange(1, 10, 2):", np.arange(1, 10, 2))

    m = analyzer.matrix

    print(f"\nMatrix element [0,0]: {m[0, 0]}")
    print(f"First row:  {m[0, :]}")
    print(f"Last row:   {m[-1, :]}")
    print(f"First col:  {m[:, 0]}")


    print("\nAbsolute values (first row):", np.abs(m[0, :]))
    print("Max absolute value in matrix:", np.max(np.abs(m)))
    print("Mean of all elements:", round(float(np.mean(m)), 2))
