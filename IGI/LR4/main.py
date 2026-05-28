"""
Lab Work #4 - Main Entry Point
Provides an interactive menu to run Tasks 1–6.

"""

from task1.task1_run  import run_task_1
from task2.task2_run  import run_task_2
from task3.task3_run  import run_task_3
from task4.task4_run  import run_task_4
from task5.task5_run  import run_task_5
from task6.task6_run  import run_task_6


def get_task_number() -> int:
    """
    Prompt the user to enter a valid task number (1–6) in a loop.

    Returns:
        int: A valid task number between 1 and 6 inclusive.
    """
    while True:
        try:
            number = int(input("\nEnter task number (1–6): "))
            if 1 <= number <= 6:
                return number
            print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


_TASK_RUNNERS = {
    1: run_task_1,
    2: run_task_2,
    3: run_task_3,
    4: run_task_4,
    5: run_task_5,
    6: run_task_6,
}


def main():
    """
    Application entry point.

    """
    print("=" * 60)
    print("  Lab Work #4 — Python: Classes, Files, Regex, NumPy, Pandas")

    print("=" * 60)

    while True:
        task_number = get_task_number()
        runner = _TASK_RUNNERS.get(task_number)
        if runner:
            runner()
        else:
            print(f"Task {task_number} is not implemented.")

        again = input("\nContinue? (y / n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
