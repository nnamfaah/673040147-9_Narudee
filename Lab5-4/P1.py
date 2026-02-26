"""
Narudee Chakitdee
673040147-9
Lab5-4
"""
import sys, os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                               QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                               QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar)
from PySide6.QtCore import QLocale
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap

try:
    import pyperclip
    has_pyperclip = True
except ImportError:
    has_pyperclip = False

default_color = "#B0E0E6"

# Full light theme applied at app level so it beats OS dark mode
light_theme = """
QWidget {
    background-color: #f0f0f0;
    color: #1a1a1a;
}
QMenuBar {
    background-color: #f0f0f0;
    color: #1a1a1a;
    border-bottom: 1px solid #cccccc;
}
QMenuBar::item { background: transparent; padding: 4px 8px; }
QMenuBar::item:selected { background-color: #d0d0d0; }
QMenu {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #cccccc;
}
QMenu::item { padding: 4px 20px; }
QMenu::item:selected { background-color: #d0e4f8; }
QToolBar {
    background-color: #f0f0f0;
    border: none;
    border-bottom: 1px solid #cccccc;
    padding: 2px;
    spacing: 4px;
}
QToolButton {
    background-color: transparent;
    color: #1a1a1a;
    border: none;
    padding: 2px 6px;
    font-size: 16px;
}
QToolButton:hover  { background-color: #d0d0d0; border-radius: 4px; }
QToolButton:pressed { background-color: #b0b0b0; border-radius: 4px; }
QStatusBar {
    background-color: #f0f0f0;
    color: #555555;
    border-top: 1px solid #cccccc;
}
QStatusBar::item { border: none; }
"""

class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(100, 100, 400, 560)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.addSpacing(5)

        # Input section
        self.input_layout = QFormLayout()
        self.input_layout.setVerticalSpacing(12)
        self.create_form()

        self.main_layout.addSpacing(5)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #cccccc; max-height: 1px;")
        self.main_layout.addWidget(line)

        self.main_layout.addSpacing(10)

        # Output / card display section
        self.bg_widget = QWidget()
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.output_layout.setContentsMargins(14, 14, 14, 14)
        self.output_layout.setSpacing(4)
        self.create_display()
        self.main_layout.addWidget(self.bg_widget)
        self.main_layout.addStretch()

        # Menu, toolbar, status bar
        self.create_menu()
        self.create_toolbar()
        self.statusBar().showMessage("Fill in your details and click generate")

    def create_form(self):
        self.name = QLineEdit()
        self.name.setPlaceholderText("First name and Lastname")

        self.age = QSpinBox()
        self.age.setRange(1, 120)
        self.age.setValue(25)

        self.email = QLineEdit()
        self.email.setPlaceholderText("username@domain.name")

        self.position = QComboBox()
        self.position.addItems(["Teaching Staff", "Supporting Staff", "Student", "Visitor"])
        self.position.setPlaceholderText("Choose your position")
        self.position.setCurrentIndex(-1)

        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        color_layout.setContentsMargins(0, 0, 0, 0)
        self.fav_color = QColor(default_color)
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(
            f"background-color: {self.fav_color.name()}; border: 1px solid #888;")
        color_layout.addWidget(self.color_swatch)
        color_button = QPushButton("Pick New Color")
        color_button.clicked.connect(self.pick_color)
        color_layout.addWidget(color_button)

        self.input_layout.addRow("Full name:", self.name)
        self.input_layout.addRow("Age:", self.age)
        self.input_layout.addRow("Email:", self.email)
        self.input_layout.addRow("Position:", self.position)
        self.input_layout.addRow("Your favorite color:", color_row)
        self.main_layout.addLayout(self.input_layout)

    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(
                f"background-color: {self.fav_color.name()}; border: 1px solid #888;")

    def create_display(self):
        self.bg_widget.setStyleSheet(
            f"background-color: {self.fav_color.name()}; border-radius: 6px;")

        self.name_label = QLabel("Your name here")
        self.name_label.setStyleSheet(
            "font-size: 18pt; font-weight: bold; background: transparent; color: #1a1a1a;")

        self.age_label = QLabel("(Age)")
        self.age_label.setStyleSheet("background: transparent; color: #1a1a1a;")

        self.position_label = QLabel("Your position here")
        self.position_label.setStyleSheet(
            "font-size: 14pt; background: transparent; color: #1a1a1a;")

        email_row = QWidget()
        email_row.setStyleSheet("background: transparent;")
        email_layout = QHBoxLayout(email_row)
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.setSpacing(6)

        email_icon = QLabel("✉")
        email_icon.setStyleSheet("font-size: 14pt; background: transparent; color: #1a1a1a;")
        self.email_label = QLabel("your_username@domain.name")
        self.email_label.setStyleSheet("background: transparent; color: #1a1a1a;")

        email_layout.addWidget(email_icon)
        email_layout.addWidget(self.email_label)
        email_layout.addStretch()

        self.output_layout.addWidget(self.name_label)
        self.output_layout.addWidget(self.age_label)
        self.output_layout.addSpacing(8)
        self.output_layout.addWidget(self.position_label)
        self.output_layout.addWidget(email_row)

    def card_text(self):
        return (f"{self.name_label.text()}\n"
                f"{self.age_label.text()}\n"
                f"{self.position_label.text()}\n"
                f"Email: {self.email_label.text()}\n")

    def update_display(self):
        self.name_label.setText(self.name.text().strip() or "Your name here")
        self.age_label.setText(f"({self.age.value()})")
        self.position_label.setText(self.position.currentText() or "Your position here")
        self.email_label.setText(self.email.text().strip() or "your_username@domain.name")
        self.bg_widget.setStyleSheet(
            f"background-color: {self.fav_color.name()}; border-radius: 6px;")
        self.statusBar().showMessage("Card generated, displaying")

    def clear_form(self):
        self.name.clear()
        self.age.setValue(25)
        self.position.setCurrentIndex(-1)
        self.email.clear()
        self.fav_color = QColor(default_color)
        self.color_swatch.setStyleSheet(
            f"background-color: {self.fav_color.name()}; border: 1px solid #888;")
        self.statusBar().showMessage("Form cleared")

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Card", "my_card.txt",
            "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, "w") as f:
                f.write(self.card_text())
            self.statusBar().showMessage(f"Card saved to {os.path.basename(filename)}")

    def clear_display(self):
        self.name_label.setText("Your name here")
        self.age_label.setText("(Age)")
        self.position_label.setText("Your position here")
        self.email_label.setText("your_username@domain.name")
        self.bg_widget.setStyleSheet(
            f"background-color: {default_color}; border-radius: 6px;")
        self.statusBar().showMessage("Display cleared")

    def copy_card(self):
        text = self.card_text()
        if has_pyperclip:
            pyperclip.copy(text)
        else:
            QApplication.clipboard().setText(text)
        self.statusBar().addPermanentWidget(QLabel("Card copied to clipboard")) # sits on the right and is never overwritten by showMessage()

    def clear_all(self):
        self.clear_form()
        self.clear_display()
        self.statusBar().showMessage("Form and display cleared")

    def create_menu(self):
        mb = self.menuBar()

        file_m = mb.addMenu("File")
        # loop tuple, lbl=str, slot=func
        for lbl, slot in [("Generate Card", self.update_display),
                           ("Save Card",     self.save_card),
                           ("Clear Display", self.clear_display)]:
            a = QAction(lbl, self); a.triggered.connect(slot); file_m.addAction(a)
        file_m.addSeparator()
        a = QAction("Exit", self); a.triggered.connect(self.close); file_m.addAction(a)

        edit_m = mb.addMenu("Edit")
        for lbl, slot in [("Copy Card", self.copy_card), ("Clear Form", self.clear_form)]:
            a = QAction(lbl, self); a.triggered.connect(slot); edit_m.addAction(a)

    def create_toolbar(self):
        tb = QToolBar()
        tb.setMovable(False) # not allow to move toolbar 
        self.addToolBar(tb)
        for icon_file, fallback, tip, slot in [
            ("generate.png", "▶",  "Generate Card",         self.update_display),
            ("save.png",     "💾", "Save Card",              self.save_card),
            ("clear.png",    "🗑", "Clear Form and Display", self.clear_all),
        ]:
            a = QAction(self)
            px = QPixmap(icon_file)
            if not px.isNull():
                a.setIcon(QIcon(px))
            else:
                a.setText(fallback)
            a.setToolTip(tip)
            a.triggered.connect(slot)
            tb.addAction(a)

def main():
    app = QApplication(sys.argv)
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))

    # Start with the full light theme, then append the QSS overrides on top
    combined = light_theme
    qss_path = "P1_style.qss"
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            combined += f.read()
    app.setStyleSheet(combined)

    window = PersonalCard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()