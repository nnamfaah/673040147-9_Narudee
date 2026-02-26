## For Master ##

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                               QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                               QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap
import sys, os

default_color = "#B0E0E6"

class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(100, 100, 400, 500)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        self.main_layout.addSpacing(15)

        # input section
        self.input_layout = QFormLayout()
        self.input_layout.setVerticalSpacing(12)
        self.create_form()

        self.main_layout.addSpacing(5)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setLineWidth(1)
        line.setStyleSheet("background-color: #cccccc;")

        self.main_layout.addSpacing(10)

        # Output section
        self.bg_widget = QWidget()
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.create_display()

        # menu
        self.create_menu()

        # toolbar
        self.create_toolbar()

        # status bar
        self.statusBar().showMessage("Fill in your details and click generate") 

    def create_form(self):
        self.name = QLineEdit()
        self.name.setPlaceholderText("First name and Lastname")
        
        self.age = QSpinBox()
        self.age.setRange(1,120)
        self.age.setValue(25)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("username@domain.name")
        
        self.position = QComboBox()
        self.position.addItems(["Teaching Staff","Supporting Staff","Student","Visitor"])
        self.position.setPlaceholderText("Choose your position")
        self.position.setCurrentIndex(-1)

        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        self.fav_color = QColor(default_color)
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(f"background-color: {self.fav_color.name()}; border: 1px solid #888;")
        color_layout.addWidget(self.color_swatch)
        color_button = QPushButton("Pick New Color")
        color_button.clicked.connect(self.pick_color)
        color_layout.addWidget(color_button)

    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(f"background-color: {self.fav_color.name()}; border: 1px solid #888;")

    def create_display(self):
    
        self.bg_widget.setStyleSheet(f"background-color: {self.fav_color.name()}; \
                                     border-radius: 6px;")

        self.name_label = QLabel("Your name here")
        self.name_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.age_label = QLabel("(Age)")
        self.position_label = QLabel("Your position here")
        self.position_label.setStyleSheet("font-size: 14pt;")
        email_icon = QLabel()
        email_icon.setPixmap(QPixmap("mail.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.email_label = QLabel("your_username@domain.name")


    def update_display(self):
        pass

    def clear_form(self):
        self.name.clear()
        self.age.setValue(25)
        self.position.setCurrentIndex(-1)
        self.email.setText("username@domain.name")
        self.bg_widget.setStyleSheet(f"background-color: {default_color}; \
                                     border-radius: 4px;")

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Card",        # dialog title
            "my_card.txt",      # default filename
            "Text Files (*.txt);;All Files (*)"  # filter
        )

        if filename:  # user didn't cancel
            with open(filename, "w") as f:
                pass

    def clear_display(self):
        self.name_label.setText("Your Name")
        self.age_label.setText(f"(Age)")
        self.position_label.setText("Your Position")
        self.email_label.setText("your_username@domain.name")
        self.bg_widget.setStyleSheet(f"background-color: {default_color}; \
                                     border-radius: 4px;")

    def copy_card(self):
        pass

    def clear_all(self):
        self.clear_form()
        self.clear_display()

    def create_menu(self):
        pass

    def create_toolbar(self):
        pass

def main():
    app = QApplication(sys.argv)

    with open("P1_style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    window = PersonalCard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()