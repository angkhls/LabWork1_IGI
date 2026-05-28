"""
Lab Work #4 - Task 5: Entry Point
Interactive runner for NumPy matrix analysis (Variant 29).
Version: 1.0
Developer: Student, Variant 29
"""

from .analyzer import MatrixAnalyzer
from .examples import demo_numpy_features


def run_task_5() -> None:
    """
    Main interactive function for Task 5.

    Prompts the user for matrix dimensions, generates a random integer matrix,
    demonstrates NumPy features, and shows Variant-29 results:
      - Sum of elements below the main diagonal
      - Standard deviation of diagonal (NumPy vs manual)
    """
    print("\n" + "=" * 50)
    print("   TASK 5 — NumPy Matrix Operations (Variant 29)")
    print("=" * 50)

    try:
        n = int(input("Enter number of rows (n >= 2): "))
        m = int(input("Enter number of cols (m >= 2): "))

        analyzer = MatrixAnalyzer(n, m)
        print("\nGenerated Matrix:")
        print(analyzer)

        stats = analyzer.get_main_stats()
        print(f"\nMatrix stats: mean={stats['mean']:.2f}, "
              f"median={stats['median']:.2f}, std={stats['std']:.2f}")

        demo_numpy_features(analyzer)

        print("\n--- Variant 29 Results ---")
        print(f"Sum of elements below main diagonal: {analyzer.sum_below_main_diagonal()}")

        std_np, std_manual = analyzer.std_diagonal_comparison()
        print(f"Std Dev of main diagonal  (NumPy) : {std_np}")
        print(f"Std Dev of main diagonal  (Manual): {std_manual}")

    except ValueError as e:
        print(f"Input error: {e}")
