"""
Lab Work #4 - Task 4: Entry Point
Interactive runner for the regular polygon figure task.
Version: 1.0
Developer: Student, Variant 29
"""

from .polygon import RegularPolygon


def run_task_4() -> None:
    """
    Main interactive function for Task 4.

    Prompts the user for polygon parameters (n, side, color, label),
    creates a RegularPolygon instance, displays calculated values,
    and saves the drawn figure to a PNG file.
    """
    print("\n--- TASK 4: Regular n-gon (Variant 29) ---")
    try:
        n     = int(input("Enter number of sides (n >= 3): "))
        side  = float(input("Enter side length (a > 0): "))
        color = input("Enter fill color (e.g. blue / red / green): ").strip() or "blue"
        label = input("Enter label text (or press Enter for default): ").strip()

        polygon = RegularPolygon(n, side, color, label)

        print(f"\n{polygon}")
        print(f"Figure type  : {polygon.get_figure_name()}")
        print(f"Total created: {RegularPolygon.count}")

        save_path = "task4/polygon.png"
        polygon.draw_and_save(save_path)
        print(f"Image saved  : {save_path}")

    except ValueError as e:
        print(f"Input error: {e}")
