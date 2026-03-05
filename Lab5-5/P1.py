"""
Narudee Chakitdee
673040147-9
P1
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QDate, QLocale
from PySide6.QtGui import QFont

class RoomCard(QWidget):
    """
    Room information card — Custom Widget Class
    Practice:
      - Inheriting QWidget
      - Signal to pass data to parent
      - select() / deselect() methods to change visual state
    """

    # Signal: emits (room_name, price) when user clicks Select
    room_selected = Signal(str, int)
    CAPACITY = {
        "Standard Room": 2,
        "Deluxe Room":   4,
        "Suite Room":    8,
        "Family Room":   4,
    }

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self._is_selected = False

        self._room_name = room_name
        self._price = price
        self._capacity = self.CAPACITY.get(room_name, 2)
        self._build_ui(emoji, description)
        self.deselect()  # Set default style

    def _build_ui(self, emoji: str, description: str):
        self.setFixedSize(200, 200)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        # Create labels and button in the card
        self.room_label = QLabel(emoji)
        self.room_label.setAlignment(Qt.AlignCenter)
        self.room_label.setFont(QFont("Segoe UI Emoji", 28))
        
        self.name_label = QLabel(self._room_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))

        self.price_label = QLabel(f"${self._price} / night")
        self.price_label.setAlignment(Qt.AlignCenter)

        self.desc_label = QLabel(description)
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: gray; front-size: 11px;")

        self.select_btn = QPushButton("Select Room")

        self.select_btn.clicked.connect(self._on_select_clicked)
        
        # Add labels and button to the layout
        layout.addWidget(self.room_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.desc_label)
        layout.addStretch()
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        """When button is clicked, emit signal to notify parent"""
        self._is_selected = True
        self.room_selected.emit(self._room_name, self._price)

    # Appearance and state when the button is selected
    def select(self):
        """Change to selected state (green border)"""

        self.setStyleSheet("""
            RoomCard {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 12px;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        """Change back to normal state"""

        self.setStyleSheet("""
            RoomCard {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
            }
            RoomCard:hover {
                border: 2px solid #6366f1;
                background-color: #f5f3ff;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

    def is_selected(self):
        return self._is_selected
    
class ConfirmDialog(QDialog):
    """
    Booking confirmation popup — Custom Dialog Class
    Practice:
      - Inheriting QDialog
      - Building layout and widgets inside the dialog manually
    """

    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 220)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        # Create labels and button in the card
        icon = QLabel("✅")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFont(QFont("Segoe UI Emoji", 30))
        
        title = QLabel("Booking Successful !")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #22c55e;")

        message = QLabel(f"Dear {guest_name},\n{room_name} is ready to welcome to you!🎉")
        message.setAlignment(Qt.AlignCenter)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(36)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border-radius: 8px;
            }
        """)
        ok_btn.clicked.connect(self.accept)

        # Add labels and button to the layout
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
        layout.addWidget(ok_btn)

# ─────────────────────────────────────────────
#  Page 1: Booking Page
# ─────────────────────────────────────────────
class BookingPage(QWidget):
    """
    Page 1 — Guest information form and room selection
    """

    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = [] # a list of RoomCard object
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        # Add widgets to the main_layout
        # Title
        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ── Section 1: Guest Info Form ──
        form_title = QLabel("📋 Guest Information")
        form_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        form_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
            }
        """)

        # Create widgets for inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. John Smith")
        self.name_input.setStyleSheet("color: black;")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. 08x-xxx-xxxx")
        self.phone_input.setMaxLength(10)
        self.phone_error = QLabel("")
        self.phone_error.setStyleSheet("color: #ef4444; font-size: 11px;")
        self.phone_input.textChanged.connect(self._validate_phone)

        self.checkin_input = QDateEdit()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        self.checkin_input.setCalendarPopup(True)

        self.checkout_input = QDateEdit()
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        self.checkout_input.setCalendarPopup(True)

        self.guests_input = QSpinBox()
        self.guests_input.setRange(1,10)
        self.guests_input.setValue(1)
        self.guests_input.setSuffix(" guest(s)")

        # Set style for inputs and their labels
        input_style = """
            QLineEdit, QDateEdit, QSpinBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #6366f1;
            }
        """
        for w in [self.name_input, self.phone_input,
                  self.checkin_input, self.checkout_input, self.guests_input]:
            w.setStyleSheet(input_style)
            w.setMinimumWidth(200)

         # create form
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)

        label_style = "font-size: 13px; color: #374151; font-weight: bold;"
        for text, widget in [
            ("Full Name :",       self.name_input),
            ("Phone Number :",    self.phone_input),
            ("Check-in Date :",   self.checkin_input),
            ("Check-out Date :",  self.checkout_input),
            ("Guests :",          self.guests_input),
        ]:
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            
            # add label and widget to your layout
            form_layout.addRow(lbl, widget)
        main_layout.addWidget(form_frame)

        # ── Section 2: Room Selection ──
        room_title = QLabel("🛏 Select a Room")
        room_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        room_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(room_title)

        rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi",             "🛏"),
            ("Deluxe Room",   120, "Double bed, Ocean view, Wi-Fi",      "🌊"),
            ("Suite Room",    250, "Living room, Jacuzzi, Premium view", "👑"),
            ("Family Room",   160, "2 Bedrooms, Perfect for families",   "👨‍👩‍👧‍👦"),
        ]
 
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Create cards according to the info above
        # Remember to put each card in self.cards
        # also catch the emitted signal from each card
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(14)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        for name, price, desc, emoji in rooms_data:
            card = RoomCard(name, price, desc, emoji)
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        self.room_error = QLabel("")
        self.room_error.setStyleSheet("color: #ef4444; font-size: 11px;")
        main_layout.addWidget(self.room_error)

        # ── Buttons ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(42)
        self.clear_btn.setFont(QFont("Segoe UI", 11))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)
        # Connect the button's signal to a slot
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next  →")
        self.next_btn.setFixedHeight(42)
        self.next_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)

    def _validate_phone(self, text: str):
        """popup an error if phone not the number or have length more than 10"""
        digits = text.replace("-", "").replace(" ", "")
        if text and not digits.isdigit():
            self.phone_error.setText("⚠ Please input only the number")
        elif text and len(digits) < 10:
            self.phone_error.setText(f"⚠ Phone number must have 10 length (Current {len(digits)} length)")
        else:
            self.phone_error.setText("")

    def _on_room_selected(self, room_name: str, price: int):
        """Receive signal from RoomCard, update state, deselect other cards"""
        guests = self.guests_input.value()

        selected_card = next((c for c in self.cards if c._room_name == room_name), None)
        capacity = selected_card._capacity if selected_card else 99

        if guests > capacity:
            self.room_error.setText(
                f"⚠ {room_name} Maximum support {capacity} person (Current {guests} person)")
            return

        self.room_error.setText("")
        self.selected_room = room_name
        self.selected_price = price

        for card in self.cards:
            if card._room_name == room_name:
                card.select()
            else:
                card.deselect()

    def clear_form(self):
        """Clear all form fields and deselect all room cards"""
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())

        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)

        self.selected_room = None
        self.selected_price = 0
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        """Collect form data — returns None if validation fails"""
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()
        guests = self.guests_input.value()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        digits = phone.replace("-", "").replace(" ", "")
        if not digits.isdigit() or len(digits) < 10:
            QMessageBox.warning(self, "Invalid Phone", "Please enter your phone number for 10 length.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates",
                                "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None
        selected_card = next((c for c in self.cards if c._room_name == self.selected_room), None)
        if selected_card and guests > selected_card._capacity:
            QMessageBox.warning(self, "Too Many Guests",
                                f"{self.selected_room} Maximum support {selected_card._capacity} person")
            return None

        nights = checkin.daysTo(checkout)
        total = nights * self.selected_price

        # Create a dictionary of all values to be returned
        return {
            "room": self.selected_room,
            "price": self.selected_price,
            "name": name,
            "phone": phone,
            "checkin": checkin.toString("dd/MM/yyyy"),
            "checkout": checkout.toString("dd/MM/yyyy"),
            "nights": nights,
            "guests": guests,
            "total": total
        }

# ─────────────────────────────────────────────
#  PAGE 2: ReviewPage
# ─────────────────────────────────────────────
class ReviewPage(QWidget):
    """
    Page 2 — Review booking details before submitting
    """

    def __init__(self):
        super().__init__()
        self.current_data = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        title = QLabel("📋 Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Please review your details before confirming")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 12px;
            }
        """)

        # You can use other layout, like a form layout
        self.info_layout = QGridLayout(self.info_frame)

        display_data = [
            ("room",     "🛏  Room"),
            ("price",    "💰  Price / Night"),
            ("name",     "👤  Guest Name"),
            ("phone",    "📞  Phone"),
            ("checkin",  "📅  Check-in"),
            ("checkout", "📅  Check-out"),
            ("nights",   "🌙  Nights"),
            ("guests",   "👥  Guests"),
        ]

        key_style = "font-weight: bold; color: #374151; font-size: 13px;"
        val_style = "color: #1f2937; font-size: 13px;"

        self.value_labels = {}

        # Put labels and placeholder into the layout
        for row, (key_name, display_text) in enumerate(display_data):
            key_lbl = QLabel(display_text)
            key_lbl.setStyleSheet(key_style)

            val_lbl = QLabel("-")
            val_lbl.setStyleSheet(val_style)

            self.info_layout.addWidget(key_lbl, row, 0)
            self.info_layout.addWidget(val_lbl, row, 1)  # ✅ correct

            self.value_labels[key_name] = val_lbl

        layout.addWidget(self.info_frame)

        # hline
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e5e7eb;")
        layout.addWidget(line)

        self.formula_label = QLabel("")
        self.formula_label.setAlignment(Qt.AlignRight)
        self.formula_label.setFont(QFont("Segoe UI", 10))
        self.formula_label.setStyleSheet("color: #6b7280;")
        layout.addWidget(self.formula_label)

        # Create the Total label and add to the layout
        self.total_label = QLabel("💳  Total Amount: $0")
        self.total_label.setAlignment(Qt.AlignRight)
        self.total_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.total_label.setStyleSheet("color: #6366f1;")
        layout.addWidget(self.total_label)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedHeight(44)
        self.back_btn.setFont(QFont("Segoe UI", 11))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 22px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)

        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        """Receive data dict from BookingPage and populate the review layout"""
        self.current_data = data    

        # Set all values from data in appropriate labels
        self.value_labels["room"].setText(data["room"])
        self.value_labels["price"].setText(f"${data['price']}")
        self.value_labels["name"].setText(data["name"])
        self.value_labels["phone"].setText(data["phone"])
        self.value_labels["checkin"].setText(data["checkin"])
        self.value_labels["checkout"].setText(data["checkout"])
        self.value_labels["nights"].setText(f"{data['nights']} night(s)")
        self.value_labels["guests"].setText(f"{data['guests']} guest(s)")

        self.formula_label.setText(
            f"${data['price']}  ×  {data['nights']} night(s)  =  ${data['total']}")
        self.total_label.setText(f"💳  Total Amount: ${data['total']}")



class MainWindow(QMainWindow):
    """
    Main window — uses QStackedWidget to manage 2 pages
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(820, 680)
        self.resize(900, 720)

        # QStackedWidget as central widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create pages
        self.booking_page = BookingPage()
        self.review_page = ReviewPage()

        self.stack.addWidget(self.booking_page)
        self.stack.addWidget(self.review_page) 

        # Add to stack: index 0 = booking, index 1 = review
        
        # Connect navigation
        # booking page: connect next_btn
        # review page: connect back_btn
        # review page: connect submit_btn
        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        # Start on page 0
        # Set current stack index to the first page
        self.stack.setCurrentIndex(0)

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0ff; }
            QScrollArea  { background-color: transparent; }
            QWidget      { font-family: 'Segoe UI', 'Tahoma', sans-serif; }
        """)

    # Slot for the next_btn on the booking page
    def _go_to_review(self):
        """Validate form, then switch to Review page"""
        
        data = self.booking_page.get_booking_data() # get booking data

        if data is None:
            return
        
        # Load data into the review page
        self.review_page.load_data(data)

        # Set stack index to the review page
        self.stack.setCurrentIndex(1)

    # Slot for the back_btn on the review page
    def _go_to_booking(self):
        """Go back to Booking page, form data remains intact"""
        self.stack.setCurrentIndex(0)

    # slot for the submit_btn on the review page
    def _on_submit(self):
        """Show ConfirmDialog, then reset the entire app"""
        data = self.review_page.current_data
        # Create a ConfirmDialog object
        # passing in the name and room
        # then show the dialog
        dialog = ConfirmDialog(data["name"], data["room"], self)
        dialog.exec()

        # Clear booking page data
        self.booking_page.clear_form()
        # Show the booking page
        self.stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()