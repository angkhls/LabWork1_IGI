"""
Lab Work #4
Defines Person and Student classes with date validation and static attributes.

"""

from datetime import datetime
from .serialization import SerializationMixin


class Person:
    """Base class representing a person with a first and last name."""

    def __init__(self, first_name: str, last_name: str):
        """
        Initialize a Person instance.

        """
        self.first_name = first_name
        self.last_name = last_name


class Student(SerializationMixin, Person):
    """
    Student class extending Person with date of birth and serialization support.
    """

    count = 0

    def __init__(self, first_name: str, last_name: str, date_str: str):
        """
        Initialize a Student instance with validated date of birth.

        """
        super().__init__(first_name, last_name)
        self.date_of_birth = date_str
        Student.count += 1

    @property
    def date_of_birth(self):
        """Get the student's date of birth as a datetime object."""
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        """
        Set the student's date of birth with validation.

        """
        if isinstance(value, datetime):
            self._date_of_birth = value
            return
        try:
            self._date_of_birth = datetime.strptime(value, "%d.%m.%Y")
        except (ValueError, TypeError):
            raise ValueError(f"Incorrect format: {value}. Use DD.MM.YYYY")

    @property
    def month_of_birth(self):
        """Return the month number (1–12) of the student's birth date."""
        return self._date_of_birth.month

    @staticmethod
    def is_valid_date(date_string: str):
        """
        Static method: check whether a string matches the DD.MM.YYYY format.

        """
        try:
            datetime.strptime(date_string, "%d.%m.%Y")
            return True
        except Exception:
            return False

    def __str__(self):
        """Magic method: return a human-readable string representation of the student."""
        return f"{self.first_name} {self.last_name} (DOB: {self._date_of_birth.strftime('%d.%m.%Y')})"
