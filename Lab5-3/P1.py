"""
Narudee Chakitdee
673040147-9
Lab5-3 P1
"""
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QLocale
from PySide6.QtGui import QColor

# Name, Student ID
def load_students(filepath: str) -> dict[str, str]: # load student ID, name
    students = {}
    if not os.path.exists(filepath):
        return students
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip() 
            if "," in line:
                sid, name = line.split(",", 1) 
                students[sid.strip()] = name.strip()
    return students

def calculate_grade(average: float) -> str: # calculate grade for A B C D F
    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"

def grade_color(grade: str) -> QColor: # define color of grade A B C D F
    return {
        "A": QColor("#c8f7c5"),
        "B": QColor("#d4eaff"),
        "C": QColor("#fff9c4"),
        "D": QColor("#ffe0b2"),
        "F": QColor("#ffcdd2"),
    }.get(grade, QColor("#ffffff"))


# Main Window
class StudentGradeCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Student scores and grades")
        self.setMinimumSize(QSize(900, 600))

        # load student data
        script_dir = os.path.dirname(os.path.abspath(__file__)) # find the path of this file
        self.students = load_students(os.path.join(script_dir, "students.txt")) # load date name, student ID

        self._build_ui() # create UI
        self._apply_styles() # add color

    # UI construction

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central) # set the main widget
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # input card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(16, 16, 16, 16)

        # Row 1: ID + Name
        row1 = QHBoxLayout()
        row1.setSpacing(16)

        student_id = QLabel("Student ID:")
        student_id.setObjectName("fieldLabel")
        self.id_combo = QComboBox()
        self.id_combo.setObjectName("idCombo")
        self.id_combo.addItem("-- Select Student ID --", userData=None)
        for sid in sorted(self.students.keys()): # loop for sort the student ID
            self.id_combo.addItem(sid, userData=sid) # add drop down ID
        self.id_combo.currentIndexChanged.connect(self._on_id_changed) # if it change will call the method

        student_name = QLabel("Student Name:")
        student_name.setObjectName("fieldLabel")
        self.name_display = QLabel("")
        self.name_display.setObjectName("nameDisplay")
        self.name_display.setMinimumWidth(220)

        row1.addWidget(student_id)
        row1.addWidget(self.id_combo, 1)
        row1.addSpacing(24)
        row1.addWidget(student_name)
        row1.addWidget(self.name_display, 2)

        # Row 2: Scores
        row2 = QHBoxLayout()
        row2.setSpacing(16)

        def make_spin(label_text): # functions add Label + Spinbox
            lbl = QLabel(label_text)
            lbl.setObjectName("fieldLabel")
            spin = QSpinBox()
            spin.setObjectName("scoreSpin")
            spin.setRange(0, 100) # define range
            spin.setValue(0)
            spin.setFixedWidth(80)
            return lbl, spin

        math, self.math_spin = make_spin("Math Score:")
        sci,  self.sci_spin  = make_spin("Science Score:")
        eng,  self.eng_spin  = make_spin("English Score:")

        for w in (math, self.math_spin, sci, self.sci_spin, eng, self.eng_spin):
            row2.addWidget(w)
        row2.addStretch()

        card_layout.addLayout(row1)
        card_layout.addLayout(row2)
        root.addWidget(card)

        # buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.btn_add   = QPushButton("Add Student")
        self.btn_reset = QPushButton("Reset Input")
        self.btn_clear = QPushButton("Clear All")

        for btn, obj in ((self.btn_add, "btnAdd"),
                         (self.btn_reset, "btnReset"),
                         (self.btn_clear, "btnClear")):
            btn.setObjectName(obj)
            btn.setFixedHeight(42)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn_row.addWidget(btn)

        self.btn_add.clicked.connect(self._add_student)
        self.btn_reset.clicked.connect(self._reset_input)
        self.btn_clear.clicked.connect(self._clear_all)

        root.addLayout(btn_row)

        # table
        self.table = QTableWidget()
        self.table.setObjectName("dataTable")
        headers = ["Student ID", "Name", "Math", "Science", "English",
                   "Total", "Average", "Grade"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)

        root.addWidget(self.table, 1)

        # internal data: {student_id: row_dict}
        self._data: dict[str, dict] = {}

    # slots

    def _on_id_changed(self, index):
        sid = self.id_combo.currentData()
        self.name_display.setText(self.students.get(sid, "") if sid else "")

    def _add_student(self):
        sid = self.id_combo.currentData()
        if not sid:
            return  # nothing selected

        name  = self.students.get(sid, "Unknown")
        math  = self.math_spin.value()
        sci   = self.sci_spin.value()
        eng   = self.eng_spin.value()
        total = math + sci + eng
        avg   = total / 3
        grade = calculate_grade(avg)

        self._data[sid] = {
            "name": name, "math": math, "sci": sci, "eng": eng,
            "total": total, "avg": avg, "grade": grade
        }
        self._refresh_table()
        self._reset_input()

    def _reset_input(self):
        self.id_combo.setCurrentIndex(0)
        self.name_display.setText("")
        self.math_spin.setValue(0)
        self.sci_spin.setValue(0)
        self.eng_spin.setValue(0)

    def _clear_all(self):
        self._data.clear()
        self.table.setRowCount(0)

    def _refresh_table(self):
        # Sort by student ID
        sorted_ids = sorted(self._data.keys())
        self.table.setRowCount(len(sorted_ids))

        for row, sid in enumerate(sorted_ids):
            d = self._data[sid]
            values = [
                sid, d["name"],
                str(d["math"]), str(d["sci"]), str(d["eng"]),
                str(d["total"]), f"{d['avg']:.2f}", d["grade"]
            ]
            color = grade_color(d["grade"])
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                # Highlight low scores red
                if col in (2, 3, 4):
                    score = int(val)
                    if score < 50:
                        item.setBackground(QColor("#ffcdd2"))
                    else:
                        item.setBackground(QColor("#ffffff"))
                elif col == 7:  # Grade column
                    item.setBackground(color)
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.table.setItem(row, col, item)

    # stylesheet

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                color: #2d3748;
            }

            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #2b6cb0;
                padding: 8px 0;
            }

            QLabel#nameDisplay {
                background: #ebf8ff;
                border: 1px solid #90cdf4;
                border-radius: 5px;
                padding: 4px 10px;
                min-height: 28px;
                color: #2c5282;
                font-style: italic;
            }

            QComboBox#idCombo {
                background: #ffffff;
                border: 1.5px solid #90cdf4;
                border-radius: 5px;
                padding: 4px 8px;
                min-height: 28px;
            }
            QComboBox#idCombo:focus {
                border-color: #3182ce;
            }
            QComboBox#idCombo::drop-down {
                border: none;
                width: 24px;
            }

            QSpinBox#scoreSpin {
                background: #ffffff;
                border: 1.5px solid #90cdf4;
                border-radius: 5px;
                padding: 4px 6px;
                min-height: 28px;
            }
            QSpinBox#scoreSpin:focus {
                border-color: #3182ce;
            }

            QPushButton#btnAdd {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#btnAdd:hover  { background: #3182ce; }
            QPushButton#btnAdd:pressed{ background: #2c5282; }

            QPushButton#btnReset {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#btnReset:hover  { background: #3182ce; }
            QPushButton#btnReset:pressed{ background: #2c5282; }

            QPushButton#btnClear {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#btnClear:hover  { background: #3182ce; }
            QPushButton#btnClear:pressed{ background: #2c5282; }

            QTableWidget#dataTable {
                background: #ffffff;
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                gridline-color: #e2e8f0;
                alternate-background-color: #f7fafc;
            }
            QTableWidget#dataTable::item:selected {
                background: #bee3f8;
                color: #2c5282;
            }
            QHeaderView::section {
                background: transparent;
                color: #2d3748;
                padding: 8px 4px;
                font-weight: bold;
                font-size: 13px;
                border-bottom: 1px solid #cbd5e0;
                border-right: 1px solid #e2e8f0;
            }
            QHeaderView::section:last {
                border-right: none;
            }
            QScrollBar:vertical {
                background: #edf2f7;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #90cdf4;
                border-radius: 5px;
            }
        """)

if __name__ == "__main__":
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

    app = QApplication(sys.argv)
    window = StudentGradeCalculator()
    window.show()
    sys.exit(app.exec())