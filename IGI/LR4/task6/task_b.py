"""
Lab Work #4 - Task 6B: Statistical Analysis (Variant 28)
Pandas indexing, extraction and statistical methods on Spotify 2023 dataset.

"""

import pandas as pd
import numpy as np


class SpotifyStatAnalyzer:
    """
    Performs statistical analysis on the Spotify DataFrame.

    Demonstrates:
      - .info() / .describe() — general DataFrame information
      - .loc / .iloc — label and positional indexing
      - Statistical methods: mean, median, std, var, corr
      - Percentile-based filtering
      - Ratio computation between extreme subgroups

    Class attributes:
        HIGH_PERCENTILE (float): Upper percentile for "most popular".
        LOW_PERCENTILE  (float): Lower percentile for "least popular".
    """

    HIGH_PERCENTILE: float = 90.0
    LOW_PERCENTILE: float = 10.0

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df (pd.DataFrame): Cleaned Spotify DataFrame.
        """
        self._df = df

    def show_dataframe_info(self) -> None:
        """
        Print shape, dtypes, non-null counts, and descriptive statistics
        for the full dataset.
        """
        print("\n[B-1] General DataFrame information")
        print("-" * 45)
        print(f"Shape: {self._df.shape[0]:,} rows × {self._df.shape[1]} columns")
        print(f"\nColumn names:\n  {list(self._df.columns)}")

        print("\nDtype per column:")
        for col, dtype in self._df.dtypes.items():
            non_null = self._df[col].notna().sum()
            print(f"  {col:<30} {str(dtype):<10} non-null: {non_null}")

        numeric_df = self._df.select_dtypes(include="number")
        print("\nDescriptive statistics (numeric columns):")
        print(numeric_df.describe().round(2).to_string())

    def show_indexing_examples(self) -> None:
        """
        Demonstrate various Pandas indexing techniques:
          - .iloc for positional access
          - .loc for label-based access with boolean mask
          - Column subset selection
        """
        print("\n[B-2] Indexing and data extraction examples")
        print("-" * 45)

        print(".iloc[0:5, 0:4] — first 5 rows, first 4 columns:")
        print(self._df.iloc[0:5, 0:4].to_string())

        mask_2023 = self._df["released_year"] == 2023
        df_2023 = self._df.loc[mask_2023, ["track_name", "artist(s)_name", "streams"]]
        print(f"\n.loc[released_year == 2023] — {len(df_2023)} tracks found, showing 5:")
        print(df_2023.head().to_string(index=False))

        top_streams = self._df.loc[
            self._df["streams"] == self._df["streams"].max(),
            ["track_name", "artist(s)_name", "streams"],
        ]
        print(f"\nMost-streamed track:\n{top_streams.to_string(index=False)}")


    def show_statistical_methods(self) -> None:
        """
        Apply and print NumPy / Pandas statistical functions:
        mean, median, std, var, correlation coefficients.
        """
        print("\n[B-3] Statistical methods")
        print("-" * 45)

        audio_cols = [
            "danceability_%", "valence_%", "energy_%",
            "acousticness_%", "liveness_%", "speechiness_%",
        ]
        audio_df = self._df[audio_cols]

        print("Mean of audio features:")
        print(audio_df.mean().round(2).to_string())

        print("\nMedian of audio features:")
        print(audio_df.median().round(2).to_string())

        print("\nStd deviation of audio features:")
        print(audio_df.std().round(2).to_string())

        print("\nVariance of audio features:")
        print(audio_df.var().round(2).to_string())

        print("\nCorrelation matrix (audio features ↔ streams):")
        corr_cols = audio_cols + ["streams"]
        corr = self._df[corr_cols].corr()
        print(corr["streams"].round(4).to_string())

    def task_b_variant28(self) -> float:
        """

          Determine how many times the average danceability of the most
          popular tracks (streams > 90th percentile) is greater than
          the average danceability of the least popular tracks
          (streams < 10th percentile).

        Returns:
            float: The ratio, rounded to 2 decimal places.
        """
        print("\n[B-4] Variant 28 — Danceability ratio: top vs bottom by streams")
        print("-" * 45)

        p_high = self._df["streams"].quantile(self.HIGH_PERCENTILE / 100)
        p_low  = self._df["streams"].quantile(self.LOW_PERCENTILE / 100)

        high_mask = self._df["streams"] > p_high
        low_mask  = self._df["streams"] < p_low

        df_high = self._df.loc[high_mask]
        df_low  = self._df.loc[low_mask]

        mean_dance_high = df_high["danceability_%"].mean()
        mean_dance_low  = df_low["danceability_%"].mean()

        ratio = round(mean_dance_high / mean_dance_low, 2)

        print(f"Streams threshold (top {self.HIGH_PERCENTILE}th pct) : {p_high:,.0f}")
        print(f"Streams threshold (low {self.LOW_PERCENTILE}th pct)  : {p_low:,.0f}")
        print(f"\nTracks in high-popularity group : {len(df_high)}")
        print(f"Tracks in low-popularity group  : {len(df_low)}")
        print(f"\nMean danceability (high pop)    : {mean_dance_high:.2f}%")
        print(f"Mean danceability (low pop)     : {mean_dance_low:.2f}%")
        print(
            f"\n>>> Avg danceability of top-popularity tracks is "
            f"{ratio}× that of low-popularity tracks"
        )

        return ratio

    def show_yearly_danceability(self) -> None:
        """
        Group by released_year, compute mean danceability and streams.
        Shows how musical characteristics evolved over time in the dataset.
        """
        print("\n[B-5] Yearly average danceability and streams")
        print("-" * 45)

        yearly = (
            self._df
            .groupby("released_year")[["danceability_%", "streams"]]
            .mean()
            .round(2)
            .sort_index()
        )
        print(yearly.to_string())


    def run_all(self) -> None:
        """Run all Task B analyses in sequence."""
        self.show_dataframe_info()
        self.show_indexing_examples()
        self.show_statistical_methods()
        self.task_b_variant28()
        self.show_yearly_danceability()
