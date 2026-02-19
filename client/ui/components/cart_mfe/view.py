from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from models.types import CartItem
from ui.styles.theme import CURRENT_THEME


# =============================================================================
# CartItemCard - Product card with pill-shaped quantity controls
# =============================================================================

class CartItemCard(QFrame):
    """
    Single product card: [Icon] [Name + Price] [−  2  +]
    Quantity controls are wrapped in a connected pill container.
    """

    def __init__(self, item: CartItem, on_plus, on_minus, parent=None):
        super().__init__(parent)
        self.item = item
        self.on_plus = on_plus
        self.on_minus = on_minus
        self._build()

    def _build(self):
        T = CURRENT_THEME

        self.setObjectName("cart_card")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            #cart_card {{
                background-color: {T.BG_CART_CARD};
                border: 1px solid {T.BORDER_SUBTLE};
                border-radius: 10px;
            }}
            #cart_card:hover {{
                background-color: {T.BG_CART_CARD_HOVER};
                border-color: {T.BORDER_COLOR};
            }}
        """)

        # Subtle elevation shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 14, 14, 14)
        row.setSpacing(14)

        # --- Product icon placeholder ---
        icon = QLabel("🛒")
        icon.setFixedSize(46, 46)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(f"""
            background-color: {T.BG_INPUT};
            border-radius: 23px;
            font-size: 22px;
        """)

        # --- Info column (Name + Price) ---
        info = QVBoxLayout()
        info.setSpacing(4)
        info.setContentsMargins(0, 0, 0, 0)

        name = QLabel(self.item.name)
        name.setWordWrap(True)
        name.setStyleSheet(f"""
            color: {T.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 600;
            background: transparent;
        """)

        price = QLabel(f"₪{self.item.price:.2f}")
        price.setStyleSheet(f"""
            color: {T.ACCENT_COLOR};
            font-size: 13px;
            font-weight: 700;
            background: transparent;
        """)

        info.addWidget(name)
        info.addWidget(price)
        info.addStretch()

        # --- Pill-shaped quantity controls ---
        qty_pill = QFrame()
        qty_pill.setObjectName("qty_pill")
        qty_pill.setStyleSheet(f"""
            #qty_pill {{
                background-color: {T.BG_INPUT};
                border-radius: 18px;
                border: 1px solid {T.BORDER_SUBTLE};
            }}
        """)
        qty_pill.setFixedHeight(36)

        pill_row = QHBoxLayout(qty_pill)
        pill_row.setContentsMargins(4, 2, 4, 2)
        pill_row.setSpacing(0)

        btn_minus = QPushButton("−")
        btn_minus.setFixedSize(30, 30)
        btn_minus.setCursor(Qt.PointingHandCursor)
        btn_minus.setToolTip("Decrease quantity")
        btn_minus.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 15px;
                color: {T.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {T.ACCENT_COLOR};
                color: white;
            }}
        """)
        btn_minus.clicked.connect(lambda: self.on_minus(self.item.id))

        qty_label = QLabel(str(self.item.quantity))
        qty_label.setAlignment(Qt.AlignCenter)
        qty_label.setFixedWidth(28)
        qty_label.setStyleSheet(f"""
            color: {T.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 700;
            background: transparent;
        """)

        btn_plus = QPushButton("+")
        btn_plus.setFixedSize(30, 30)
        btn_plus.setCursor(Qt.PointingHandCursor)
        btn_plus.setToolTip("Increase quantity")
        btn_plus.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 15px;
                color: {T.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {T.ACCENT_COLOR};
                color: white;
            }}
        """)
        btn_plus.clicked.connect(lambda: self.on_plus(self.item.id))

        pill_row.addWidget(btn_minus)
        pill_row.addWidget(qty_label)
        pill_row.addWidget(btn_plus)

        # Center-align the pill vertically
        qty_wrapper = QVBoxLayout()
        qty_wrapper.addStretch()
        qty_wrapper.addWidget(qty_pill)
        qty_wrapper.addStretch()

        # --- Assemble card ---
        row.addWidget(icon)
        row.addLayout(info, 1)
        row.addLayout(qty_wrapper)


# =============================================================================
# CartView - Full cart panel
# =============================================================================

class CartView(QWidget):
    """
    Premium cart panel with product cards, pill-quantity controls,
    beautiful empty state, and prominent "Find Cheapest Store" button.
    """

    item_incremented = Signal(str)
    item_decremented = Signal(str)
    optimize_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        T = CURRENT_THEME

        self.setStyleSheet(f"background-color: {T.BG_SIDEBAR};")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # === HEADER ===
        header = QWidget()
        header.setStyleSheet(f"""
            background: transparent;
            border-bottom: 1px solid {T.BORDER_SUBTLE};
        """)
        hl = QVBoxLayout(header)
        hl.setContentsMargins(16, 20, 16, 16)
        hl.setSpacing(6)

        title = QLabel("🛒  Shopping Cart")
        title.setStyleSheet(f"""
            color: {T.TEXT_PRIMARY};
            font-size: 17px;
            font-weight: bold;
            background: transparent;
        """)

        self.store_name_label = QLabel("No store selected")
        self.store_name_label.setStyleSheet(f"""
            color: {T.TEXT_PRIMARY};
            font-size: 13px;
            font-weight: 600;
            background: transparent;
        """)

        self.store_address_label = QLabel("")
        self.store_address_label.setWordWrap(True)
        self.store_address_label.setStyleSheet(f"""
            color: {T.TEXT_SECONDARY};
            font-size: 12px;
            background: transparent;
        """)

        hl.addWidget(title)
        hl.addWidget(self.store_name_label)
        hl.addWidget(self.store_address_label)

        # === ITEMS SCROLL AREA ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.items_container = QWidget()
        self.items_container.setStyleSheet(f"background-color: {T.BG_SIDEBAR};")

        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(12, 12, 12, 12)
        self.items_layout.setSpacing(10)
        self.items_layout.addStretch()  # Sentinel

        # Initial empty state
        self._empty_widget = self._make_empty_state(T)
        self.items_layout.insertWidget(0, self._empty_widget)

        self.scroll_area.setWidget(self.items_container)

        # === FOOTER ===
        footer = QWidget()
        footer.setStyleSheet(f"""
            background-color: {T.BG_SIDEBAR};
            border-top: 1px solid {T.BORDER_SUBTLE};
        """)
        fl = QVBoxLayout(footer)
        fl.setContentsMargins(16, 16, 16, 16)
        fl.setSpacing(14)

        # Total row
        total_row = QHBoxLayout()
        tl = QLabel("Total")
        tl.setStyleSheet(f"""
            color: {T.TEXT_SECONDARY};
            font-size: 14px;
            background: transparent;
        """)
        self.total_price_label = QLabel("₪0.00")
        self.total_price_label.setStyleSheet(f"""
            color: {T.TEXT_PRIMARY};
            font-size: 22px;
            font-weight: bold;
            background: transparent;
        """)
        total_row.addWidget(tl)
        total_row.addStretch()
        total_row.addWidget(self.total_price_label)

        # Optimize button
        self.optimize_btn = QPushButton("🔍  Find Cheapest Store")
        self.optimize_btn.setCursor(Qt.PointingHandCursor)
        self.optimize_btn.setMinimumHeight(48)
        self.optimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {T.ACCENT_COLOR};
                border: none;
                border-radius: 12px;
                padding: 14px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover  {{ background-color: {T.ACCENT_HOVER}; }}
            QPushButton:pressed {{ background-color: {T.ACCENT_PRESSED}; }}
            QPushButton:disabled {{
                background-color: {T.BG_QUANTITY_BTN};
                color: {T.TEXT_TERTIARY};
            }}
        """)
        self.optimize_btn.clicked.connect(self.optimize_clicked.emit)

        fl.addLayout(total_row)
        fl.addWidget(self.optimize_btn)

        # === ASSEMBLE ===
        root.addWidget(header)
        root.addWidget(self.scroll_area, 1)
        root.addWidget(footer)

    # --- Empty state ---
    @staticmethod
    def _make_empty_state(T) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        lay.setContentsMargins(20, 48, 20, 48)
        lay.setSpacing(12)

        icon = QLabel("🛒")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 52px; background: transparent;")

        title = QLabel("Your cart is empty")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            color: {T.TEXT_TERTIARY};
            font-size: 15px;
            font-weight: 600;
            background: transparent;
        """)

        hint = QLabel("Add items by chatting with the AI")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"""
            color: {T.TEXT_TERTIARY};
            font-size: 12px;
            background: transparent;
        """)

        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(hint)
        return w

    # --- Public API (presenter contract) ---

    def render_cart(self, store_name: str, address: str, items: list, total_price: float):
        """
        Render the full cart. Preserves original interface signature.
        """
        T = CURRENT_THEME

        # Update header
        self.store_name_label.setText(store_name if store_name else "No store selected")
        self.store_address_label.setText(address or "")

        # Update total
        self.total_price_label.setText(f"₪{total_price:.2f}")

        # Clear existing items (keep stretch at end)
        while self.items_layout.count() > 1:
            child = self.items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not items:
            self._empty_widget = self._make_empty_state(T)
            self.items_layout.insertWidget(0, self._empty_widget)
        else:
            for i, item in enumerate(items):
                card = CartItemCard(
                    item,
                    on_plus=self.item_incremented.emit,
                    on_minus=self.item_decremented.emit
                )
                self.items_layout.insertWidget(i, card)