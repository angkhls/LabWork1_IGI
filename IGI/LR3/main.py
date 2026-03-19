# Lab work #3: Standard data types, collections, functions, modules
# Main module: task selection and testing
# Version: 1.0
# Developer: Student
# Date: 2025

from task1.power_series import math_ln, calculate_ln
from task2.find_min_value import find_min_value
from task3.count_letters import count_of_letters_numbers
from task4.text_analysis import task_4
from task5.ListProcessing import run_task_5


def get_task_number():
    """
    Prompts the user to enter a valid task number (1–5).
    Repeats until a valid integer in range is entered.

    Returns:
        int: task number chosen by the user
    """
    while True:
        try:
            number = int(input("Enter task number (1-5): "))
            if 1 <= number <= 5:
                return number
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def run_task_1():
    """Runs task 1: computes ln(1-x) via power series and compares with math.log."""
    while True:
        try:
            x = float(input("Enter x (|x| must be < 1): "))
            result, n = calculate_ln(x)
            math_result = math_ln(x)
            print("-" * 90)
            print(f"x = {x}  |  n = {n}  |  F(x) = {result}  |  math F(x) = {math_result}")
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")


def ask_continue():
    """
    Asks the user whether to exit the program.

    Returns:
        bool: True to continue, False to exit
    """
    answer = input("Press 0 to exit, or any other key to continue: ").strip()
    return answer != "0"


def main():
    """
    Entry point. Shows a menu, runs the chosen task, and repeats
    until the user decides to quit.
    """
    print("=" * 60)
    print("  Lab work #3 — Python tasks")
    print("=" * 60)

    task_number = get_task_number()
    keep_running = True

    while keep_running:
        match task_number:
            case 1:
                print("\n--- Task 1: Power series ln(1-x) ---")
                run_task_1()

            case 2:
                print("\n--- Task 2: Find minimum and sum ---")
                find_min_value()

            case 3:
                print("\n--- Task 3: Count lowercase letters and digits ---")
                count_of_letters_numbers()

            case 4:
                print("\n--- Task 4: Text analysis ---")
                task_4()

            case 5:
                print("\n--- Task 5: List processing ---")
                run_task_5()

        keep_running = ask_continue()
        if keep_running:
            task_number = get_task_number()


if __name__ == "__main__":
    main()






