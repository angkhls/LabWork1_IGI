"""
Lab Work #4 - Task 6: Entry Point
"""

import os

from .data_loader import SpotifyDataLoader
from .task_a import SpotifySeriesAnalyzer
from .task_b import SpotifyStatAnalyzer

_DEFAULT_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "spotify-2023.csv",
)


def _ask_csv_path():
    """
    Prompt the user for the dataset path.
    Defaults to the project-root 'spotify-2023.csv' if the user presses Enter.
    """
    print(f"\nDefault dataset path: {os.path.abspath(_DEFAULT_CSV)}")
    user_input = input(
        "Enter path to spotify-2023.csv [press Enter to use default]: "
    ).strip()
    return user_input if user_input else _DEFAULT_CSV


def _print_menu():

    print("\n" + "-" * 50)
    print("  Task 6 sub-menu:")
    print("  1 — Task A : Series, DataFrame, rolling stats")
    print("  2 — Task B : Statistical analysis ")
    print("  3 — Both A and B")
    print("  0 — Return to main menu")
    print("-" * 50)


def run_task_6():
    """
    Main interactive function for Task 6.

    Loads the Spotify 2023 CSV dataset via SpotifyDataLoader,
    then lets the user run Task A (Series/DataFrame demos) and/or
    Task B (statistical analysis), including the Variant-28 specific questions.
    """
    print("\n" + "=" * 50)
    print("   TASK 6 — Pandas: Spotify 2023 Dataset")
    print("=" * 50)

    while True:
        try:
            csv_path = _ask_csv_path()
            loader = SpotifyDataLoader(csv_path)
            df = loader.df
            print(f"\nDataset loaded successfully!")
            print(loader)
            break
        except FileNotFoundError as exc:
            print(f"\nError: {exc}")
            retry = input("Try a different path? (y/n): ").strip().lower()
            if retry != "y":
                print("Returning to main menu.")
                return
        except Exception as exc:
            print(f"\nUnexpected error while loading dataset: {exc}")
            return

    analyzer_a = SpotifySeriesAnalyzer(df)
    analyzer_b = SpotifyStatAnalyzer(df)

    while True:
        _print_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            analyzer_a.run_all()
        elif choice == "2":
            analyzer_b.run_all()
        elif choice == "3":
            analyzer_a.run_all()
            analyzer_b.run_all()
        elif choice == "0":
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please enter 0, 1, 2, or 3.")
