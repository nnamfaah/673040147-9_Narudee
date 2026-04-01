import json
import pandas as pd
import pyqtgraph as pg

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]

# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    To do 1 — Read a CSV file and return a clean DataFrame.
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The CSV file is empty.")
    missing = REQUIRED_COLS - set(df.columns)

    if missing:
        raise ValueError(f"The CSV file is missing required columns: {missing}")
    
    return df

def read_json(path: str) -> pd.DataFrame:
    """
    To do 2 — Read a JSON file and return a DataFrame.
    """
    df = pd.read_json(path)

    if df.empty:
        raise ValueError("The JSON file is empty.")
    missing = REQUIRED_COLS - set(df.columns)

    if missing:
        raise ValueError(f"The JSON file is missing required columns: {missing}")
    
    return df

def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    To do 3 — Save a DataFrame to a CSV file.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot write to CSV.")
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        raise IOError(f"An error occurred while writing to CSV: {e}")

def write_json(df: pd.DataFrame, path: str) -> None:
    """
    To do 4 — Save a DataFrame to a JSON file.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot write to JSON.")
    try:
        df.to_json(path, orient='records', indent=4)
    except Exception as e:
        raise IOError(f"An error occurred while writing to JSON: {e}")

def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    To do 5 — Return a summary string shown in the Statistics panel.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot build statistics.")
    missing = REQUIRED_COLS - set(df.columns)

    if missing:
        raise ValueError(f"The DataFrame is missing required columns: {', '.join(missing)}")

    stats = df.groupby("city").agg(
        count        = ("temp_c",      "count"),
        avg_temp     = ("temp_c",      "mean"),
        max_temp     = ("temp_c",      "max"),
        min_temp     = ("temp_c",      "min"),
        total_rain   = ("rainfall_mm", "sum"),
        avg_humidity = ("humidity",    "mean"),
    ).round(1)

    cities_present = [c for c in CITIES if c in stats.index]
    stats = stats.reindex(cities_present)
 
    row_labels = ["count", "avg_temp", "max_temp", "min_temp", "total_rain", "avg_humidity"]
    row_display = [
        "Records",
        "Avg Temp (°C)",
        "Max Temp (°C)",
        "Min Temp (°C)",
        "Total Rain (mm)",
        "Avg Humidity (%)",
    ]
 
    n_rows = len(row_labels)
    n_cols = len(cities_present) + 1  # +1 for the row labels

    table = QTableWidget(n_rows, n_cols)
    table.setHorizontalHeaderLabels(["Statistic"] + cities_present)
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setAlternatingRowColors(True)
 
    header_font = QFont()
    header_font.setBold(True)

    for ri, (key, label) in enumerate(zip(row_labels, row_display)):
        label_item = QTableWidgetItem(label)
        label_item.setFont(header_font)
        label_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table.setItem(ri, 0, label_item)

        for ci, city in enumerate(cities_present):
            val = stats.loc[city, key]
            if key == "count":
                text = str(int(val))
            else:
                text = f"{val:.1f}"
            cell = QTableWidgetItem(text)
            cell.setTextAlignment(Qt.AlignCenter)
            table.setItem(ri, ci + 1, cell)
 
    table.resizeColumnsToContents()
    table.horizontalHeader().setFont(header_font)
 
    return table

def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    To do 6 — Draw a Rainfall Histogram chart using pyqtgraph and return a PlotWidget.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot show chart.")
    
    if "rainfall_mm" not in df.columns:
        raise ValueError("The DataFrame is missing the 'rainfall_mm' column required for the chart.")

    import numpy as np
    values = df["rainfall_mm"].dropna().values
    counts, bin_edges = np.histogram(values, bins=10)
 
    plot_widget = pg.PlotWidget()
    plot_widget.setBackground("w")
    plot_widget.setTitle("Rainfall Histogram", color="k", size="12pt")
    plot_widget.setLabel("left",   "Frequency",     color="k", size="10pt")
    plot_widget.setLabel("bottom", "Rainfall (mm)", color="k", size="10pt")
    plot_widget.showGrid(x=True, y=True, alpha=0.3)  

    bar_item = pg.BarGraphItem(
        x=bin_edges[:-1],
        height=counts,
        width=(bin_edges[1] - bin_edges[0]) * 0.9,
        brush=pg.mkBrush(100, 149, 237, 200),   # cornflower blue
        pen=pg.mkPen("w", width=0.5),
    )
    plot_widget.addItem(bar_item)
 
    return plot_widget