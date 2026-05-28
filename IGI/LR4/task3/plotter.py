"""
Lab Work #4 - Task 3
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


class SeriesPlotter:
    """Static helper class for plotting and saving series convergence charts."""

    @staticmethod
    def plot_and_save(calculator, output_dir: str = "task3_results") -> str:
        """
        Plot the partial sums of the series against the exact math value and save to PNG.


        """
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "series_plot.png")

        n_vals = list(range(1, calculator.n_terms + 1))
        stats  = calculator.get_stats()

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(n_vals, calculator.series_values, 'b-o',
                label=f"Series ln(1-x), x={calculator.x}", markersize=4)

        ax.axhline(y=calculator.math_value, color='r', linestyle='--',
                   label=f"Exact value: {calculator.math_value:.6f}")

        stats_text = (
            f"Mean:   {stats['mean']:.4f}\n"
            f"Median: {stats['median']:.4f}\n"
            f"StDev:  {stats['stdev']:.4f}"
        )
        ax.text(0.02, 0.05, stats_text, transform=ax.transAxes,
                bbox=dict(facecolor='wheat', alpha=0.5), fontsize=9)

        ax.set_xlabel("Number of terms (n)")
        ax.set_ylabel("Partial sum F(x)")
        ax.set_title(f"Variant 29: ln(1-x) — Series vs Exact Value (x={calculator.x})")
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path
