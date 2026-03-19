# Lab work #3: Standard data types, collections, functions, modules
# Task 2: Find minimum value and sum of entered numbers
# Version: 1.0
# Developer: Khlus Anhelina
# Date: 19.03.26


def find_min_value():
    """
    Reads integers from user input until 1 is entered.
    Prints the minimum value and the sum of all entered numbers.
    Handles invalid (non-integer) input gracefully.
    """
    numbers = []
    print("Enter integers one by one. Enter 1 to stop.")
    while True:
        try:
            num = int(input("Enter number: "))
            if num == 1:
                break
            numbers.append(num)
        except ValueError:
            print("Error: please enter a valid integer.")

    if numbers:
        print(f"Min value of numbers = {min(numbers)}")
        print(f"Sum of numbers = {sum(numbers)}")
    else:
        print("No numbers were entered.")