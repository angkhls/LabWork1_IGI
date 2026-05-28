"""
Lab Work #4 - Task 2: Advanced Text Analyzer (Variant 29)
"""

import re
from .base import TextProcessor


class AdvancedTextAnalyzer(TextProcessor):
    """
    Variant-29 text analyzer.

    Adds:
      - find_words_mixed:   words containing lowercase letters AND digits
      - is_valid_ip:        validate an IPv4 address string
      - count_lowercase:    count all lowercase letters in the text
      - find_first_v_word:  find first word containing the letter 'v'
      - exclude_s_words:    remove all words starting with 's' or 'S'
    """

    def find_words_mixed(self):
        """
        Find all words that contain at least one lowercase letter AND at least one digit.

        Uses lookaheads to enforce both conditions simultaneously.

        Returns:
            list[str]: Words matching the mixed lowercase-letter + digit pattern.
        """
        pattern = r'\b(?=[a-zа-яё\d]*[a-zа-яё])(?=[a-zа-яё\d]*\d)[a-zа-яё\d]+\b'
        return re.findall(pattern, self.text)

    def is_valid_ip(self, ip_string: str):
        """
        Check whether ip_string is a valid decimal IPv4 address.

        Returns:
            bool: True if the string is a valid IPv4 address, False otherwise.
        """
        octet = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        pattern = rf'^{octet}\.{octet}\.{octet}\.{octet}$'
        return re.match(pattern, ip_string) is not None

    def count_lowercase(self):
        """
        Count the total number of lowercase letters (Latin and Cyrillic) in the text.

        Returns:
            int: Number of lowercase letter characters found.
        """
        return len(re.findall(r'[a-zа-яё]', self.text))

    def find_first_v_word(self):
        """
        Find the first word containing the letter 'v'
        """
        words = re.findall(r'\b[a-zа-яё]+\b', self.text, flags=re.IGNORECASE)
        for index, word in enumerate(words, 1):
            if 'v' in word.lower():
                return word, index
        return None, None

    def exclude_s_words(self):
        """
        Return the text with all words starting with 's' or 'S' removed.

        Returns:
            str: Cleaned text without any s-initial words.
        """
        return re.sub(r'\b[sS][a-zа-яё]*\b\s*', '', self.text).strip()
