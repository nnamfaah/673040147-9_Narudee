from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap
from style import C
class StudentCard(QFrame):
    # Signal for delete request: emits self
    delete_requested = Signal(object)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data

        # for drag and drop
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self._build()

    def _build(self):
        # height depends on number of courses selected
        courses = [
            c for c in [
                self.data.get("course1", ""),
                self.data.get("course2", ""),
                self.data.get("course3", ""),
            ]
            if c and not c.startswith("—")]

        # base height: name + dept rows, plus 18px per course line
        self.setMinimumHeight(70 + len(courses) * 20)

        self.setStyleSheet(f"""
            QFrame {{
                background:{C['card']};
            }}
            QFrame:hover {{
                background:{C['surface']};
            }}
        """)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(8)

        # drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(f"background:transparent; color:{C['muted']};font-size:18px;padding-top:2px;")

        info = QVBoxLayout()
        info.setSpacing(2)
        info.setContentsMargins(0, 0, 0, 0)

        name_row = QHBoxLayout()
        name_row.setSpacing(8)
        
        lbl_name = QLabel(self.data.get("fullname", ""))
        lbl_name.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl_name.setStyleSheet(f"color:{C['text']};background:transparent;")
 
        lbl_id = QLabel(self.data.get("student_id", ""))
        lbl_id.setStyleSheet(f"color:{C['muted']};font-size:11px;background:transparent;")
 
        name_row.addWidget(lbl_name)
        name_row.addWidget(lbl_id)
        name_row.addStretch()

        lbl_dept = QLabel(f"{self.data.get('faculty','')}  ·  {self.data.get('major','')}")
        lbl_dept.setStyleSheet(f"color:{C['muted']};font-size:12px;background:transparent;")
 
        info.addLayout(name_row)
        info.addWidget(lbl_dept)

        for c in courses:
            lbl_c = QLabel(c)
            lbl_c.setStyleSheet(f"color:{C['text']};font-size:12px;background:transparent;")
            info.addWidget(lbl_c)

        # delete button
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(28, 28)
        btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent;
                color:{C['muted']};
                border:none;
                border-radius:14px;
                font-size:11px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']};
                color:white;
                border:none;
            }}""")
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))

        outer.addWidget(handle, alignment=Qt.AlignTop)
        outer.addLayout(info, stretch=1)
        outer.addWidget(btn_del, alignment=Qt.AlignTop)

    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)