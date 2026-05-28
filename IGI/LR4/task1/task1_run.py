
from .models import Student
from .school_class import SchoolClass


def choose_saving_method(school_class: SchoolClass):

    if not school_class.student_list:
        print("No students to save.")
        return

    sample = school_class.student_list[0]
    while True:
        try:
            choice = int(input("\nSelect save format (1 = CSV, 2 = Pickle): "))
            if choice == 1:
                filename = "students.csv"
                sample.save_to_csv(filename, school_class.student_list)
                print(f"Saved to {filename}")
                break
            elif choice == 2:
                filename = "students.pkl"
                sample.save_to_pickle(filename, school_class.student_list)
                print(f"Saved to {filename}")
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")
        except Exception as e:
            print(f"Error saving file: {e}")


def run_task_1():

    print("\n--- TASK 1: Student Management (Variant 29) ---")
    class_name = input("Enter class name: ")
    school_class = SchoolClass(class_name)

    try:
        n = int(input("How many students to add? "))
        if n <= 0:
            print("Error: number of students must be positive.")
            return
    except ValueError:
        print("Invalid input: please enter a positive integer.")
        return

    for i in range(n):
        print(f"\nStudent #{i + 1}:")
        first_name = input("  First name: ")
        last_name  = input("  Last name:  ")
        dob        = input("  Birth date (DD.MM.YYYY): ")
        try:
            school_class.add_student(Student(first_name, last_name, dob))
        except ValueError as e:
            print(f"  Error: {e}. Student not added.")

    print(f"\nTotal students registered: {Student.count}")

    try:
        month = int(input("\nEnter birth month to search (1–12): "))
        results = school_class.student_born_in_specific_month(month)
        if results:
            print(f"Students born in month {month}:")
            for s in results:
                print(f"  {s}")
        else:
            print(f"No students found for month {month}.")
    except ValueError:
        print("Invalid month input.")
        return

    choose_saving_method(school_class)
