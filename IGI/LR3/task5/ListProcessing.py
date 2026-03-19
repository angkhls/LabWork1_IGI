# Lab work #3: Standard data types, collections, functions, modules
# Task 5: Real number list processing — find product of negative elements
#         and sum of positive elements located before the maximum element
# Version: 1.0
# Developer: Student
# Date: 2025

import random


# ── Initialisation module ────────────────────────────────────────────────────

def init_from_user(lst):
    """
    Initialises a list with float values entered by the user.
    Validates each input and asks again on invalid entry.
    The user first specifies the desired list size.

    Args:
        lst: list to fill (will be cleared first)
    """
    lst.clear()
    while True:
        try:
            size = int(input("Enter the number of elements: "))
            if size <= 0:
                print("Size must be a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    print(f"Enter {size} real numbers:")
    for i in range(size):
        while True:
            try:
                value = float(input(f"  Element [{i}]: "))
                lst.append(value)
                break
            except ValueError:
                print("Invalid input. Please enter a real number.")


def init_from_generator(lst):
    """
    Initialises a list using a generator function that produces random floats.
    The user specifies the list size; values are in the range [-10.0, 10.0].

    Args:
        lst: list to fill (will be cleared first)
    """
    lst.clear()
    while True:
        try:
            size = int(input("Enter the number of elements to generate: "))
            if size <= 0:
                print("Size must be a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    lst.extend(random_float_generator(size))


def random_float_generator(n):
    """
    Generator function that yields n random float values in [-10.0, 10.0].

    Args:
        n: number of values to generate

    Yields:
        float: a random float rounded to 2 decimal places
    """
    for _ in range(n):
        yield round(random.uniform(-10.0, 10.0), 2)


# ── Display ──────────────────────────────────────────────────────────────────

def print_list(lst):
    """
    Prints all elements of the list with their indices.

    Args:
        lst: the list to display
    """
    if not lst:
        print("List is empty.")
        return
    print("List elements:")
    for i, val in enumerate(lst):
        print(f"  [{i}] {val}")


# ── Main task logic ──────────────────────────────────────────────────────────

def product_of_negatives(lst):
    """
    Computes the product of all negative elements in the list.

    Args:
        lst: list of floats

    Returns:
        float: product of negative elements, or None if there are no negatives
    """
    negatives = [x for x in lst if x < 0]
    if not negatives:
        return None
    product = 1.0
    for x in negatives:
        product *= x
    return product


def sum_positives_before_max(lst):
    """
    Computes the sum of positive elements located BEFORE the maximum element.

    Args:
        lst: list of floats

    Returns:
        float: the sum, or None if the maximum is at index 0 or the list is empty
    """
    if not lst:
        return None
    max_index = lst.index(max(lst))
    if max_index == 0:
        return None
    return sum(x for x in lst[:max_index] if x > 0)


def run_task_5():
    """
    Main function for task 5.
    Asks the user to choose an initialisation method, displays the list,
    then prints the product of negative elements and the sum of positive
    elements before the maximum element.
    """
    numbers = []

    print("\n--- Task 5: List processing ---")
    print("Choose initialisation method:")
    print("  1 — Enter values manually")
    print("  2 — Generate values automatically")

    while True:
        choice = input("Your choice (1 or 2): ").strip()
        if choice == "1":
            init_from_user(numbers)
            break
        elif choice == "2":
            init_from_generator(numbers)
            break
        else:
            print("Please enter 1 or 2.")

    print_list(numbers)

    neg_product = product_of_negatives(numbers)
    if neg_product is None:
        print("Product of negative elements: no negative elements found.")
    else:
        print(f"Product of negative elements = {neg_product}")

    pos_sum = sum_positives_before_max(numbers)
    if pos_sum is None:
        print("Sum of positive elements before maximum: not applicable "
              "(maximum is the first element or list is empty).")
    else:
        print(f"Sum of positive elements before maximum element = {pos_sum}")