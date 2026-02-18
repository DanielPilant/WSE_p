from PySide6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem, 
                               QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt, Signal
from models.types import CartItem

class CartItemRow(QWidget):
    def __init__(self, item: CartItem, on_plus, on_minus):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(12)
        
        self.lbl_name = QLabel(item.name)
        
        self.lbl_price = QLabel(f"{item.price} NIS")
        
        self.btn_minus = QPushButton("-")
        self.btn_minus.setFixedWidth(32)
        self.btn_minus.clicked.connect(lambda: on_minus(item.id))
        
        self.lbl_qty = QLabel(str(item.quantity))
        self.lbl_qty.setAlignment(Qt.AlignCenter)
        self.lbl_qty.setFixedWidth(40)
    
        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedWidth(32)
        self.btn_plus.clicked.connect(lambda: on_plus(item.id))

        layout.addWidget(self.lbl_name, 2)
        layout.addWidget(self.lbl_price, 1)
        layout.addWidget(self.btn_minus)
        layout.addWidget(self.lbl_qty)
        layout.addWidget(self.btn_plus)
        self.setLayout(layout)

class CartView(QWidget):
    item_incremented = Signal(str)
    item_decremented = Signal(str)
    optimize_clicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        self.header_lbl = QLabel("The cart is empty")
        self.header_lbl.setWordWrap(True)
        
        self.items_list = QListWidget()
        
        self.footer_lbl = QLabel("Total: 0.00 NIS")
        
        self.optimize_btn = QPushButton("🔄 Find Cheapest Store")
        self.optimize_btn.setCursor(Qt.PointingHandCursor)
        self.optimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; 
                color: white; 
                font-weight: bold; 
                padding: 8px; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.optimize_btn.clicked.connect(self.optimize_clicked.emit)
        
        layout.addWidget(self.header_lbl)
        layout.addWidget(self.items_list)
        layout.addWidget(self.footer_lbl)
        layout.addWidget(self.optimize_btn)
        
        self.setLayout(layout)

    def render_cart(self, store_name, address, items, total_price):
        self.header_lbl.setText(f"Best value at: {store_name}\n{address}")
        self.footer_lbl.setText(f"Total to pay: {total_price:.2f} NIS")
        
        self.items_list.clear()
        for item in items:
            list_item = QListWidgetItem(self.items_list)
            row_widget = CartItemRow(
                item, 
                on_plus=self.item_incremented.emit, 
                on_minus=self.item_decremented.emit
            )
            list_item.setSizeHint(row_widget.sizeHint())
            self.items_list.setItemWidget(list_item, row_widget)