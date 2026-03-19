
# Lab work #3: Standard data types, collections, functions, modules
# Task 3: Count lowercase letters and digits in a string
# Version: 1.0
# Developer: Student
# Date: 2025


def count_of_letters_numbers():
    """
    Reads a string from the user and counts:
      - the number of lowercase letters
      - the number of digits
    Prints both counts to the console.
    """
    user_str = input("Enter a string: ")

    lower_count = 0
    numbers_count = 0

    for char in user_str:
        if char.islower():
            lower_count += 1
        if char.isdigit():
            numbers_count += 1

    print(f"Count of lowercase letters = {lower_count}")
    print(f"Count of digits = {numbers_count}")
