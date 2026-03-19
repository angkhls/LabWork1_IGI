# Lab work #3: Standard data types, collections, functions, modules
# Task 4: Text analysis — words with odd letter count, shortest word starting
#         with 'i', repeated words
# Version: 1.0
# Developer: Student
# Date: 2025

TEXT = ("So she was considering in her own mind, as well as she could, for the hot day made her feel "
        "very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the "
        "trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes "
        "ran close by her.")


def section_divider(func):
    """
    Decorator that prints a divider line before and after the wrapped function's output.
    Demonstrates decorator usage as required by lab task.
    """

    def wrapper(*args, **kwargs):
        print("-" * 60)
        result = func(*args, **kwargs)
        print("-" * 60)
        return result

    return wrapper


def get_words(text):
    """
    Returns a list of clean lowercase words from the text.
    Strips punctuation characters from both ends of each token.

    Args:
        text: input string

    Returns:
        list of str: cleaned lowercase words
    """
    words = []
    for word in text.split():
        clean = word.strip(".,!?;:-").lower()
        if clean:
            words.append(clean)
    return words


@section_divider
def odd_letter_words(text):
    """
    Finds total word count and prints words with an odd number of letters.

    Args:
        text: input string to analyse
    """
    words = get_words(text)
    print(f"Total words: {len(words)}")
    odd_words = [w for w in words if len(w) % 2 != 0]
    print(f"Words with odd letter count: {odd_words}")


@section_divider
def shortest_word_starting_with_i(text):
    """
    Finds and prints the shortest word that starts with the letter 'i'.

    Args:
        text: input string to analyse
    """
    words = get_words(text)
    i_words = [w for w in words if w.startswith("i")]
    if i_words:
        shortest = min(i_words, key=len)
        print(f"Shortest word starting with 'i': {shortest}")
    else:
        print("No words starting with 'i' found.")


@section_divider
def repeated_words(text):
    """
    Finds and prints all repeated (duplicate) words in the text.

    Args:
        text: input string to analyse
    """
    words = get_words(text)
    seen = set()
    repeated = set()
    for word in words:
        if word in seen:
            repeated.add(word)
        seen.add(word)
    if repeated:
        print(f"Repeated words: {sorted(repeated)}")
    else:
        print("No repeated words found.")


def task_4():
    """
    Main function for task 4 — performs full text analysis on the built-in TEXT string.
    Calls three analysis sub-functions, each decorated with a section divider.
    """
    odd_letter_words(TEXT)
    shortest_word_starting_with_i(TEXT)
    repeated_words(TEXT)