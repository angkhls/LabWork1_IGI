"""
Lab Work #4 - Task 3
"""

from .calculator import SeriesCalculator
from .plotter import SeriesPlotter


def run_task_3() -> None:
    """
    Main interactive function for Task 3.

    Prompts the user for x and the number of terms, computes the Taylor
    series for ln(1-x), prints statistics, and saves the convergence plot.
    """
    print("\n--- TASK 3: Series Expansion ln(1-x) (Variant 29) ---")
    print(f"Formula: {SeriesCalculator.FORMULA_STR}")
    try:
        x = float(input("Enter x  (|x| < 1): "))
        n = int(input("Enter number of terms n (>= 1): "))

        calc  = SeriesCalculator(x, n)
        stats = calc.get_stats()

        print(f"\nResults for x={x}, n={n}:")
        print(f"  Series approximation : {calc.final_value:.8f}")
        print(f"  Exact math.log value : {calc.math_value:.8f}")
        print(f"  Error (epsilon)      : {calc.epsilon:.2e}")
        print(f"  Mean of partial sums : {stats['mean']:.8f}")
        print(f"  Median               : {stats['median']:.8f}")
        print(f"  Mode                 : {stats['mode']}")
        print(f"  Variance             : {stats['variance']:.8f}")
        print(f"  Std deviation        : {stats['stdev']:.8f}")

        plot_path = SeriesPlotter.plot_and_save(calc)
        print(f"\nConvergence plot saved to: {plot_path}")

    except ValueError as e:
        print(f"Input error: {e}")
