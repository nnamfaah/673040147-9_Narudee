"""
Narudee Chakitdee
6730040147-9
Lab 4-3 P2
"""

from datetime import datetime

class Person:
    def __init__(self, name, age, birthdate):
        self.name = name
        self.age = age
        self._birthdate = birthdate
        self._id = self.__generate_id()
        self.__bloodgroup = None
        self.__is_married = False

    def __generate_id(self):
        current_year = datetime.now().year
        running_number = 1  # This should be managed to ensure uniqueness
        return f"{current_year}{running_number:03d}"

    def display_info(self):
        return f"Name: {self.name}, Age: {self.age}, ID: {self._id}"

class Staff(Person):
    def __init__(self, name, age, birthdate, department, start_year):
        super().__init__(name, age, birthdate)
        self.department = department
        self.start_year = start_year
        self.tenure_year = self.__calculate_tenure_year()
        self.__salary = 0 # Name mangling for private attribute

    def __calculate_tenure_year(self):
        current_year = datetime.now().year
        return current_year - self.start_year

    def set_salary(self, salary):
        self.__salary = salary

    def get_salary(self):
        return self.__salary

    def display_info(self):
        return f"{super().display_info()}, Department: {self.department}, Tenure Year: {self.tenure_year}, Salary: {self.__salary}"

class Professor(Staff):
    def __init__(self, name, age, birthdate, department, start_year, professorship, admin_position=0):
        super().__init__(name, age, birthdate, department, start_year)
        self.professorship = professorship
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        self.salary = 30000 + self.tenure_year * 1000 + self.professorship * 10000 + self.admin_position * 10000

    def display_info(self):
        return f"{super().display_info()}, Professorship: {self.professorship}, Admin Position: {self.admin_position}"

class Administrator(Staff):
    def __init__(self, name, age, birthdate, department, start_year, admin_position):
        super().__init__(name, age, birthdate, department, start_year)
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        self.__salary = 15000 + self.tenure_year * 800 + self.admin_position * 5000

    def display_info(self):
        return f"{super().display_info()}, Admin Position: {self.admin_position}"

class Student(Person):
    def __init__(self, name, age, birthdate, start_year, major, level, grade_list=None):
        super().__init__(name, age, birthdate)
        self.start_year = start_year
        self.major = major
        self.level = level
        self.grade_list = grade_list if grade_list is not None else []
        self.gpa = self.__calculate_gpa()
        self.__graduation_date = self.__calculate_graduation_date()

    @staticmethod
    def calculate_gpa(credit_grade_pairs):
        total_points = 0
        total_credits = 0
        for credit, grade in credit_grade_pairs:
            total_points += credit * grade
            total_credits += credit
        return total_points / total_credits if total_credits > 0 else 0

    def __calculate_gpa(self):
        return self.calculate_gpa(self.grade_list)

    def __calculate_graduation_date(self):
        if self.level == "undergraduate":
            return self.start_year + 4
        elif self.level == "graduate":
            return self.start_year + 2
        return None

    def display_info(self):
        return f"{super().display_info()}, Major: {self.major}, Level: {self.level}, GPA: {self.gpa}, Graduation Date: {self.__graduation_date}"

class UndergraduateStudent(Student):
    def __init__(self, name, age, birthdate, start_year, major, level, club, course_list=None):
        super().__init__(name, age, birthdate, start_year, major, level, grade_list=None)
        self.club = club
        self.course_list = course_list if course_list is not None else []

    def register_course(self, course):
        self.course_list.append(course)

    def display_info(self):
        return f"{super().display_info()}, Club: {self.club}, Courses: {self.course_list}"

class GraduateStudent(Student):
    def __init__(self, name, age, birthdate, start_year, major, level, advisor_name, thesis_name=None, proposal_date=None, grade_list=None):
        super().__init__(name, age, birthdate, start_year, major, level, grade_list)
        self.advisor_name = advisor_name
        self.thesis_name = thesis_name
        self.__proposal_date = proposal_date
        self.__graduation_date = self.__calculate_graduation_date()

    def __calculate_graduation_date(self):
        if self.__proposal_date is not None:
            return self.__proposal_date.year + 1  # 1 year from the proposal date
        else:
            return datetime.now().year + 2  # 2 years from today

    def set_thesis_name(self, thesis_name):
        self.thesis_name = thesis_name

    def set_proposal_date(self, proposal_date):
        self.__proposal_date = proposal_date
        self.__graduation_date = self.__calculate_graduation_date()  # Update graduation date

    def get_proposal_date(self):
        return self.__proposal_date

    def get_graduation_date(self):
        return self.__graduation_date

    def display_info(self):
        return (f"{super().display_info()}, Advisor: {self.advisor_name}, Thesis: {self.thesis_name}, "
                f"Proposal Date: {self.__proposal_date}, Graduation Date: {self.__graduation_date}")

if __name__ == "__main__":
    grad_student = GraduateStudent(
        name = "Narudee Chakitdee",
        age = 20,
        birthdate ="2005-08-15",
        start_year = 2023,
        major = "DME",
        level = "graduate",
        advisor_name = "Dr.navy"
    )

    grad_student.set_thesis_name("Caffeine Effect")
    grad_student.set_proposal_date(datetime(2026, 1, 1))

    print(grad_student.display_info())