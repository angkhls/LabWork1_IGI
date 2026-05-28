"""
Lab Work #4 - Task 6A:
"""

import pandas as pd
import numpy as np


class SpotifySeriesAnalyzer:
    """
    Demonstrates core Pandas Series and DataFrame capabilities.

    Covers:
      - pd.Series creation from a DataFrame column
      - .loc / .iloc access
      - Aggregation (mean, sum)
      - Rolling window statistics
      - display()-equivalent via print (console environment)

    Static attributes:
        ROLLING_WINDOW (int): Window size for rolling calculations.
        YEAR_FILTER    (int): Release year used for variant-specific task.
    """

    ROLLING_WINDOW: int = 10
    YEAR_FILTER: int = 2020

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df (pd.DataFrame): Cleaned Spotify DataFrame from SpotifyDataLoader.
        """
        self._df = df

    def demo_series_creation(self):
        """
        Show multiple ways to create a pd.Series.

        """
        print("\n[A-1] Series creation examples")
        print("-" * 45)

        s_list = pd.Series(
            ["pop", "rock", "hip-hop", "latin", "indie"],
            index=["g1", "g2", "g3", "g4", "g5"],
            name="genre_sample",
        )
        print("Series from list:\n", s_list)

        s_dict = pd.Series(
            {"danceability": 68.5, "energy": 64.3, "valence": 51.8},
            name="avg_audio_features",
        )
        print("\nSeries from dict:\n", s_dict)

        bpm_series = pd.Series(self._df["bpm"].values[:8], name="bpm_sample")
        print("\nSeries from DataFrame column (first 8 BPM values):\n", bpm_series)

    def demo_indexing(self):
        """
        Demonstrate element access via .iloc (positional) and .loc (label).
        """
        print("\n[A-2] Indexing: .iloc and .loc")
        print("-" * 45)

        sample = pd.Series(
            self._df["danceability_%"].values[:10],
            index=[f"track_{i}" for i in range(10)],
            name="danceability_%",
        )
        print("Series (10 danceability values):\n", sample)
        print(f"\n.iloc[2] (3rd element): {sample.iloc[2]}")
        print(f".loc['track_5']       : {sample.loc['track_5']}")
        print(f".iloc[3:6] (slice)    :\n{sample.iloc[3:6]}")


    def demo_dataframe_creation(self):
        """
        Show DataFrame creation from dict and from NumPy array.
        """
        print("\n[A-3] DataFrame creation")
        print("-" * 45)

        top5 = self._df.nlargest(5, "streams")[
            ["track_name", "artist(s)_name", "streams", "released_year"]
        ].reset_index(drop=True)
        print("DataFrame (top-5 most streamed tracks):")
        print(top5.to_string())

        arr = np.array([[120, 75, 85], [100, 60, 90], [130, 80, 70]])
        df_np = pd.DataFrame(arr, columns=["bpm", "energy_%", "danceability_%"],
                             index=["trackA", "trackB", "trackC"])
        print("\nDataFrame from NumPy array (synthetic):")
        print(df_np)

    def demo_aggregation(self):
        """
        Demonstrate mean, sum, and describe() on a Series.
        """
        print("\n[A-4] Aggregation on Series")
        print("-" * 45)

        streams_series = self._df["streams"]
        print(f"Total streams  : {streams_series.sum():,}")
        print(f"Mean streams   : {streams_series.mean():,.0f}")
        print(f"Median streams : {streams_series.median():,.0f}")
        print(f"Max streams    : {streams_series.max():,}")
        print(f"Min streams    : {streams_series.min():,}")

    def task_a_variant28(self):
        """
         Task A:
          Build Series popularity_2020 from streams of tracks released in 2020.
          Calculate rolling mean over ROLLING_WINDOW tracks.

        Returns:
            pd.DataFrame: With columns 'track_name', 'streams',
                          'rolling_mean_streams'.
        """
        print(f"\n[A-5] Variant 28 — Series for year {self.YEAR_FILTER} + rolling mean")
        print("-" * 45)

        mask = self._df["released_year"] == self.YEAR_FILTER
        df_year = self._df.loc[mask, ["track_name", "streams"]].copy()
        df_year.reset_index(drop=True, inplace=True)

        if df_year.empty:
            print(f"No tracks found for year {self.YEAR_FILTER}.")
            return df_year

        popularity_series = pd.Series(
            df_year["streams"].values,
            index=df_year["track_name"].values,
            name=f"streams_{self.YEAR_FILTER}",
        )

        print(f"Tracks released in {self.YEAR_FILTER}: {len(popularity_series)}")
        print(f"\nFirst 5 entries of popularity_{self.YEAR_FILTER}:")
        print(popularity_series.head())

        rolling_mean = popularity_series.rolling(
            window=self.ROLLING_WINDOW, min_periods=1
        ).mean().round(0)

        result_df = pd.DataFrame({
            "track_name": popularity_series.index,
            "streams": popularity_series.values,
            f"rolling_mean_{self.ROLLING_WINDOW}": rolling_mean.values,
        })

        print(f"\nRolling mean (window={self.ROLLING_WINDOW}) — first 15 rows:")
        print(result_df.head(15).to_string(index=False))

        return result_df

    def run_all(self):
        """Run all Task A demos in sequence."""
        self.demo_series_creation()
        self.demo_indexing()
        self.demo_dataframe_creation()
        self.demo_aggregation()
        self.task_a_variant28()
