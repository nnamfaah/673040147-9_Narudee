"""
Narudee Chakitdee
673040147-9
Lab 5-1, P2
"""
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QHBoxLayout, QLineEdit, QLabel, QPushButton,
                               QRadioButton, QButtonGroup, QComboBox, QTextEdit,
                               QCheckBox, QDateEdit)
from PySide6.QtCore import QDate, QLocale, Qt
from PySide6.QtGui import QFont

class StudentRegistration(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title label
        text_label = QLabel("Student Registration Form")
        text_label.setFont(QFont("Arial", 15, QFont.Bold))
        text_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(text_label)
        
        # Add spacing between widgets
        main_layout.addSpacing(20)

        # Full Name
        full_name = QLabel("Full Name:")
        main_layout.addWidget(full_name)
        self.name_input = QLineEdit()
        main_layout.addWidget(self.name_input)
        
        # Email
        main_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        main_layout.addWidget(self.email_input)
        
        # Phone
        main_layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        main_layout.addWidget(self.phone_input)
        
        # Date of Birth
        main_layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)  # Shows calendar dropdown
        self.date_edit.setDisplayFormat("dd/MM/yyyy")  # Format like "01/01/2000"
        self.date_edit.setDate(QDate(2000, 1, 1))  # Set default date to January 1, 2000
        self.date_edit.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        
        main_layout.addWidget(self.date_edit)
        self.date_edit.setFixedWidth(200)
        
        # Gender
        main_layout.addWidget(QLabel('Gender:'))
        
        # Button group ensures only one can be selected
        self.gender_group = QButtonGroup()
        
        radio_layout = QHBoxLayout()
        
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.nonbinary_radio = QRadioButton("Non-binary")
        self.prefer_not_radio = QRadioButton("Prefer not to say")
        
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.nonbinary_radio)
        self.gender_group.addButton(self.prefer_not_radio)
        
        radio_layout.addWidget(self.male_radio)
        radio_layout.addWidget(self.female_radio)
        radio_layout.addWidget(self.nonbinary_radio)
        radio_layout.addWidget(self.prefer_not_radio)
        
        main_layout.addLayout(radio_layout)
        
        # Add spacing between widgets
        main_layout.addSpacing(20)
        
        # Program
        main_layout.addWidget(QLabel("Program:"))
        self.program_combo = QComboBox()
        self.program_combo.addItem("Select your program")
        self.program_combo.addItems([
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electrical Engineering",
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Power Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ])
        main_layout.addWidget(self.program_combo)
        
        # Tell us about yourself
        main_layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        self.about_text = QTextEdit()
        self.about_text.setMaximumHeight(100)  # Set max height to 100
        main_layout.addWidget(self.about_text)
        
        # Add spacing between widgets
        main_layout.addSpacing(20)
        
        # Terms and conditions checkbox
        self.terms_checkbox = QCheckBox('I accept the terms and conditions.')
        main_layout.addWidget(self.terms_checkbox)
        
        # Submit button
        submit_btn = CustomButton()
        main_layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        submit_btn.clicked.connect(self.process_registration)
        
        # Add stretch to push everything to top
        main_layout.addStretch()

    def process_registration(self):
        # Get selected gender
        selected_gender = ""
        if self.male_radio.isChecked():
            selected_gender = "Male"
        elif self.female_radio.isChecked():
            selected_gender = "Female"
        elif self.nonbinary_radio.isChecked():
            selected_gender = "Non-binary"
        elif self.prefer_not_radio.isChecked():
            selected_gender = "Prefer not to say"

class CustomButton(QPushButton):
    def __init__(self):
        super().__init__()
        
        # Basic setup
        self.setText("Submit Registration")
        
        # Size configurations
        self.setFixedSize(150, 40)  # Fixed width and height
        
        # Connect signals
        self.clicked.connect(self.handle_click)
    
    def handle_click(self):
        print("Submit Registration")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2: Student Registration")
        self.setGeometry(100, 100, 400, 600)  # Window size 400 x 600
        
        # Create central widget
        central_widget = StudentRegistration()
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()