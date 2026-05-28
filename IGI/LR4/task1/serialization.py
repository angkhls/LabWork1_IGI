"""
Lab Work #4 - Task 1: Serialization Mixin
Module providing CSV and Pickle serialization for student data.

"""

import pickle
import csv
from datetime import datetime


class SerializationMixin:
    """Mixin class providing serialization functionality for student objects."""

    def save_to_pickle(self, filename: str, students: list):
        """
        Serialize a list of student objects to a binary Pickle file.

        """
        with open(filename, "wb") as f:
            pickle.dump(students, f)

    def save_to_csv(self, filename: str, students: list):
        """
        Save a list of student objects to a CSV file with headers.

        """
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['first_name', 'last_name', 'date_of_birth']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in students:
                writer.writerow({
                    'first_name': s.first_name,
                    'last_name': s.last_name,
                    'date_of_birth': s.date_of_birth.strftime('%d.%m.%Y')
                })
