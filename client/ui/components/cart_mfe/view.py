from PySide6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem, 
                               QHBoxLayout, QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal
from models.types import CartItem

# --- Helper widget for a single row (internal to View) ---
class CartItemRow(QWidget):
    def __init__(self, item: CartItem, on_plus, on_minus):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(12)
        
        self.lbl_name = QLabel(item.name)
        self.lbl_name.setStyleSheet("font-weight: 500; color: #fafafa;")
        
        self.lbl_price = QLabel(f"{item.price} NIS")
        self.lbl_price.setStyleSheet("color: #a1a1aa; font-size: 13px;")
        
        self.btn_minus = QPushButton("-")
        self.btn_minus.setProperty("class", "icon-btn")
        self.btn_minus.setFixedWidth(32)
        self.btn_minus.clicked.connect(lambda: on_minus(item.id))
        
        self.lbl_qty = QLabel(str(item.quantity))
        self.lbl_qty.setAlignment(Qt.AlignCenter)
        self.lbl_qty.setFixedWidth(40)
        self.lbl_qty.setStyleSheet("font-weight: 700; color: #6366f1; font-size: 14px;")
    
        self.btn_plus = QPushButton("+")
        self.btn_plus.setProperty("class", "icon-btn")
        self.btn_plus.setFixedWidth(32)
        self.btn_plus.clicked.connect(lambda: on_plus(item.id))

        layout.addWidget(self.lbl_name, 2)
        layout.addWidget(self.lbl_price, 1)
        layout.addWidget(self.btn_minus)
        layout.addWidget(self.lbl_qty)
        layout.addWidget(self.btn_plus)
        self.setLayout(layout)

# --- Main View ---
class CartView(QWidget):
    # Signals that the Presenter will listen to
    item_incremented = Signal(str) # sends the ID
    item_decremented = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Header
        self.header_lbl = QLabel("The cart is empty")
        self.header_lbl.setObjectName("CartHeader")
        self.header_lbl.setWordWrap(True)
        
        # Items list
        self.items_list = QListWidget()
        
        # Footer
        self.footer_lbl = QLabel("Total: 0.00 NIS")
        self.footer_lbl.setObjectName("CartFooter")
        
        layout.addWidget(self.header_lbl)
        layout.addWidget(self.items_list)
        layout.addWidget(self.footer_lbl)
        self.setLayout(layout)

    def render_cart(self, store_name, address, items, total_price):
        """Function that Presenter calls to redraw the screen"""
        self.header_lbl.setText(f"Best value at: {store_name}\n{address}")
        self.footer_lbl.setText(f"Total to pay: {total_price:.2f} NIS")
        
        self.items_list.clear()
        for item in items:
            list_item = QListWidgetItem(self.items_list)
            # Creating the row and connecting its buttons to the Main View signals
            row_widget = CartItemRow(
                item, 
                on_plus=self.item_incremented.emit, 
                on_minus=self.item_decremented.emit
            )
            list_item.setSizeHint(row_widget.sizeHint())
            self.items_list.setItemWidget(list_item, row_widget)