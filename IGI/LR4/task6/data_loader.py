"""
Lab Work #4 - Task 6
"""

import os
import pandas as pd

DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "spotify-2023.csv",
)


class SpotifyDataLoader:
    """
    Loads and lightly cleans the Spotify 2023 Kaggle dataset.

    Attributes (class-level):
        ENCODING  (str) : File encoding (latin1 to handle special chars).
        DATASET_NAME (str): Human-readable name shown in menus.
    """

    ENCODING: str = "latin1"
    DATASET_NAME: str = "Spotify Most Streamed Songs 2023"

    def __init__(self, csv_path: str = DEFAULT_CSV_PATH):
        """
        Initialize the loader with a path to the CSV file.

        Args:
            csv_path (str): Absolute or relative path to the CSV.

        Raises:
            FileNotFoundError: If the CSV does not exist at the given path.
        """
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(
                f"Dataset not found at '{csv_path}'.\n"
                "Please place 'spotify-2023.csv' in the project root."
            )
        self._csv_path = csv_path
        self._df: pd.DataFrame | None = None

    @property
    def df(self) -> pd.DataFrame:
        """Return the loaded DataFrame, loading it on first access."""
        if self._df is None:
            self._df = self._load()
        return self._df

    @property
    def csv_path(self):
        """Read-only path to the source CSV."""
        return self._csv_path

    def _load(self) -> pd.DataFrame:
        """
        Read the CSV and apply minimal cleaning.

        Cleaning steps:
          - Coerce 'streams' to numeric (some rows contain non-numeric text).
          - Drop rows where 'streams' is NaN after coercion.
          - Reset index.

        Returns:
            pd.DataFrame: Clean Spotify dataset.
        """
        df = pd.read_csv(self._csv_path, encoding=self.ENCODING)

        # 'streams' is stored as string in the raw file
        df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
        df.dropna(subset=["streams"], inplace=True)
        df["streams"] = df["streams"].astype("int64")
        df.reset_index(drop=True, inplace=True)

        return df


    def __repr__(self) -> str:
        status = "loaded" if self._df is not None else "not yet loaded"
        return f"SpotifyDataLoader(path='{self._csv_path}', status={status})"

    def __str__(self) -> str:
        if self._df is not None:
            return (
                f"{self.DATASET_NAME}\n"
                f"Rows: {len(self._df):,} | Columns: {len(self._df.columns)}\n"
                f"Path: {self._csv_path}"
            )
        return f"{self.DATASET_NAME} — not yet loaded"
