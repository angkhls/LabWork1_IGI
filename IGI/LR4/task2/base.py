"""
Lab Work #4 - Task 2
"""

import re


class TextProcessor:
    """Base class for loading a text file and performing regex-based analysis."""

    def __init__(self, input_filename: str):
        self.text = ""
        self.input_filename = input_filename
        self._load_text()

    def _load_text(self):
        """
        read the file content into self.text
        """
        try:
            with open(self.input_filename, 'r', encoding='utf-8') as f:
                self.text = f.read()
        except FileNotFoundError:
            print(f"Error: file '{self.input_filename}' not found.")

    def find_sentences(self):
        """
        Count the total number of sentences in the text.
        Returns:
            int: Number of sentences detected.
        """
        return len(re.findall(r'[^.!?]+[.!?]+', self.text))

    def find_sentences_by_type(self):
        """
        Count sentences of each type separately:
          - declarative:   end with '.'
          - interrogative: end with '?'
          - exclamatory:   end with '!'

        """
        declarative   = len(re.findall(r'[^.!?]+\.+', self.text))
        interrogative = len(re.findall(r'[^.!?]+\?+', self.text))
        exclamatory   = len(re.findall(r'[^.!?]+!+',  self.text))
        return {
            'declarative':   declarative,
            'interrogative': interrogative,
            'exclamatory':   exclamatory,
        }

    def avg_sentence_length(self):
        """
        Calculate the average sentence length in characters,
        counting only letters
        Returns Average number of letter-characters per sentence,

        """
        sentences = re.findall(r'[^.!?]+[.!?]+', self.text)
        if not sentences:
            return 0.0
        lengths = [len(re.findall(r'[a-zа-яёA-ZА-ЯЁ]', s)) for s in sentences]
        return sum(lengths) / len(lengths)

    def count_smiles(self):
        """
        Detect smiley-face sequences according to the lab specification.

        """
        pattern = r'[;:]-*(?P<br>[()\[\]])(?P=br)*'
        full_smiles = [m.group() for m in re.finditer(pattern, self.text)]
        return len(full_smiles), full_smiles

    def avg_word_length(self):
        """
        Calculate the average word length (letters only) in the text.

        """
        words = re.findall(r'[a-zа-яё]+', self.text, flags=re.IGNORECASE)
        if not words:
            return 0.0
        return sum(len(w) for w in words) / len(words)
