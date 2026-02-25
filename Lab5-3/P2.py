"""
Narudee Chakitdee
673040147-9
Lab5-3 P2
"""
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox,
    QGroupBox, QDoubleSpinBox)
from PySide6.QtCore import Qt, QLocale
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
categories = ["Electronics", "Clothing", "Food", "Others"]
colors = {
    "Electronics": "#4C72B0",
    "Clothing":    "#DD8452",
    "Food":        "#55A868",
    "Others":      "#C44E52",
}

class SalesChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Chart")
        self.resize(900, 650)
        # data structure: {category: {month: amount}}
        self.data = {cat: {m: 0 for m in months} for cat in categories}

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # ---- Left panel (controls) ----
        left = QWidget()
        left.setFixedWidth(260)
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignTop)

        # File group
        file_group = QGroupBox("Import Data")
        file_layout = QVBoxLayout(file_group)
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("e.g. sales_data.txt")
        self.import_btn = QPushButton("Import Data")
        self.import_btn.clicked.connect(self.import_data)
        file_layout.addWidget(QLabel("Filename:"))
        file_layout.addWidget(self.filename_input)
        file_layout.addWidget(self.import_btn)

        # Input group
        input_group = QGroupBox("Add Sales Record")
        input_layout = QVBoxLayout(input_group)

        self.month_combo = QComboBox()
        self.month_combo.addItems(months)

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0, 10_000_000)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setSingleStep(100)
        self.amount_spin.setPrefix("฿ ")

        self.category_combo = QComboBox()
        self.category_combo.addItems(categories)

        self.add_btn = QPushButton("Add Data")
        self.add_btn.clicked.connect(self.add_data)

        self.clear_btn = QPushButton("Clear Chart")
        self.clear_btn.clicked.connect(self.clear_chart)
        self.clear_btn.setStyleSheet("color: red;")

        input_layout.addWidget(QLabel("Month:"))
        input_layout.addWidget(self.month_combo)
        input_layout.addWidget(QLabel("Sales Amount:"))
        input_layout.addWidget(self.amount_spin)
        input_layout.addWidget(QLabel("Product Category:"))
        input_layout.addWidget(self.category_combo)
        input_layout.addSpacing(8)
        input_layout.addWidget(self.add_btn)
        input_layout.addWidget(self.clear_btn)

        left_layout.addWidget(file_group)
        left_layout.addSpacing(10)
        left_layout.addWidget(input_group)

        # ---- Right panel (chart) ----
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(left)
        main_layout.addWidget(self.canvas, stretch=1)
        self.plot_chart()

    def import_data(self):
        filename = self.filename_input.text().strip()
        if not filename:
            QMessageBox.warning(self, "Error", "Please enter a filename.")
            return
        if not os.path.exists(filename):
            QMessageBox.warning(self, "File Not Found",
                                f"File '{filename}' does not exist.")
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 3:
                        raise ValueError(f"Line {line_no}: expected 3 fields, got {len(parts)}")
                    month, amount_str, category = parts
                    if month not in months:
                        raise ValueError(f"Line {line_no}: unknown month '{month}'")
                    if category not in categories:
                        raise ValueError(f"Line {line_no}: unknown category '{category}'")
                    amount = float(amount_str)
                    self.data[category][month] += amount
            self.plot_chart()
            QMessageBox.information(self, "Success", f"Data imported from '{filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", str(e))

    def add_data(self):
        month = self.month_combo.currentText()
        amount = self.amount_spin.value()
        category = self.category_combo.currentText()
        self.data[category][month] += amount
        self.plot_chart()

    def clear_chart(self):
        reply = QMessageBox.question(self, "Clear Chart",
                                     "Are you sure to clear all data?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.data = {cat: {m: 0 for m in months} for cat in categories}
            self.plot_chart()

    def plot_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = np.arange(len(months))
        n_cats = len(categories)
        bar_width = 0.2
        offsets = np.linspace(-(n_cats - 1) / 2, (n_cats - 1) / 2, n_cats) * bar_width

        for i, cat in enumerate(categories):
            values = [self.data[cat][m] for m in months]
            ax.bar(x + offsets[i], values, width=bar_width,
                   label=cat, color=colors[cat], alpha=0.85)

        ax.set_title("Monthly Sales by Product Category", fontsize=14, fontweight="bold")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales Amount (฿)")
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend(title="Category", loc="upper right")
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
        )
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    app = QApplication(sys.argv)
    window = SalesChartApp()
    window.show()
    sys.exit(app.exec())