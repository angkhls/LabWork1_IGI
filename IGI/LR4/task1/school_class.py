from .models import Student

class SchoolClass:
    """Class for controll student list for one class """

    def __init__(self, class_name):
        self.class_name = class_name
        self.student_list = []

    def add_student(self, student):
        if isinstance(student, Student):
            self.student_list.append(student)

    def student_born_in_specific_month(self, month):
        return [s for s in self.student_list if s.month_of_birth == month]