from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QFrame, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtCore import QThreadPool, Qt, QPropertyAnimation, QEasingCurve
from ui.components.cart_mfe.presenter import CartPresenter
from ui.components.chat_mfe.presenter import ChatPresenter
from ui.components.user_mfe.presenter import UserPresenter
from data.repositories.supermarket_repo import SupermarketRepository
from ui.dialogs.ambiguity_dialog import AmbiguityDialog
from core.workers import AIWorker, CartOptimizeWorker, CartUpdateWorker
from core.user_manager import UserManager
from models.types import ClarificationRequest, StoreResult
from ui.styles.theme import get_all_stylesheets, CURRENT_THEME


class AppController(QMainWindow):
    
    # This is the central controller of the application, responsible for:
    # 1. Managing the overall UI layout and state (sidebar, chat, cart)
    # 2. Handling user interactions and routing them to the appropriate presenters and repositories
    # 3. Coordinating background workers for API calls to keep the UI responsive
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supermarket AI Agent")
        self.resize(1400, 800)
        self.setMinimumSize(960, 600)
        
        # Apply all stylesheets
        self.setStyleSheet(get_all_stylesheets())
        
        # --- Data & State Layer ---
        self.repo = SupermarketRepository()
        #self.user_manager = UserManager() 
        
        # --- Presentation Layer ---
        self.chat_presenter = ChatPresenter() # No repo needed for chat presenter since it only displays text and sends user input back to the controller
        self.cart_presenter = CartPresenter(self.repo) # We pass the repo to the cart presenter because it needs to trigger updates when quantities change
        
        # Connect cart item change signal to update worker
        self.cart_presenter.cart_item_changed.connect(self.handle_cart_update)
        
        # Connect optimize button signal
        self.cart_presenter.optimize_requested.connect(self.handle_optimize_request)

        # --- Wiring / Logic Flow ---
        self.chat_presenter.user_input_submitted.connect(self.handle_user_message)
        
        # --- Sidebar state ---
        self.sidebar_expanded = True
        self.sidebar_animation = None
        
        # --- UI Construction ---
        self.setup_ui()
        
        # --- Bootstrap ---
        self.user_manager.login_guest()
        
        print("Initializing session with Agent...")
        is_connected = self.repo.initialize_session()
        
        if not is_connected:
            self.chat_presenter.display_agent_response("⚠️ Warning: Could not connect to the Agent server. Is it running on port 8001?")
        else:
            self.chat_presenter.display_agent_response("Hi! I'm your AI shopping assistant. What would you like to add to your cart today?")

    # ============= UI Construction Methods =================================================================
    def setup_ui(self):
        """Build the 3-column layout: Sidebar, Chat, Cart"""
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {CURRENT_THEME.BG_MAIN};")
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === 1. LEFT SIDEBAR ===
        self.sidebar_container = self._create_sidebar()
        
        # === 2. CENTER CHAT AREA ===
        chat_container = self._create_chat_area()
        
        # === 3. RIGHT CART PANEL ===
        cart_container = self._create_cart_panel()

        # Assemble the layout
        main_layout.addWidget(self.sidebar_container)
        main_layout.addWidget(chat_container, 1)  # stretch factor 1
        main_layout.addWidget(cart_container)
        
    # ============= UI Component Creation Methods ===========================================================
    def _create_sidebar(self):
        """Create the collapsible sidebar with history placeholder"""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar_container")
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(f"""
            #sidebar_container {{
                background-color: {CURRENT_THEME.BG_SIDEBAR};
                border-right: 1px solid {CURRENT_THEME.BORDER_SUBTLE};
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Top row with hamburger toggle
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        
        self.btn_toggle_sidebar = QPushButton("☰")
        self.btn_toggle_sidebar.setObjectName("sidebar_toggle_btn")
        self.btn_toggle_sidebar.setFixedSize(40, 40)
        self.btn_toggle_sidebar.setCursor(Qt.PointingHandCursor)
        self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar)
        self.btn_toggle_sidebar.setStyleSheet(f"""
            QPushButton {{
                background: transparent; 
                border: none; 
                font-size: 20px;
                color: {CURRENT_THEME.TEXT_SECONDARY};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {CURRENT_THEME.BG_SIDEBAR_HOVER};
                color: {CURRENT_THEME.TEXT_PRIMARY};
            }}
        """)
        
        top_row.addWidget(self.btn_toggle_sidebar)
        top_row.addStretch()
        
        layout.addLayout(top_row)
        
        # New Chat button
        new_chat_btn = QPushButton("  ✨  New Chat")
        new_chat_btn.setObjectName("new_chat_btn")
        new_chat_btn.setCursor(Qt.PointingHandCursor)
        new_chat_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {CURRENT_THEME.BORDER_COLOR};
                border-radius: 8px;
                padding: 12px 16px;
                color: {CURRENT_THEME.TEXT_PRIMARY};
                text-align: left;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {CURRENT_THEME.BG_SIDEBAR_HOVER};
            }}
        """)
        layout.addWidget(new_chat_btn)
        
        # Divider
        layout.addSpacing(16)
        
        # History section label
        history_label = QLabel("History")
        history_label.setObjectName("sidebar_section_label")
        history_label.setStyleSheet(f"""
            color: {CURRENT_THEME.TEXT_TERTIARY};
            font-size: 12px;
            padding: 8px 4px;
        """)
        layout.addWidget(history_label)
        
        # History scroll area
        history_scroll = QScrollArea()
        history_scroll.setWidgetResizable(True)
        history_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        history_scroll.setStyleSheet("border: none; background: transparent;")
        
        history_content = QWidget()
        history_content.setStyleSheet("background: transparent;")
        history_layout = QVBoxLayout(history_content)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(4)
        
        # Placeholder history items
        placeholder_items = [
            "🛒 Shopping list for dinner",
            "🥗 Healthy meal prep",
            "🎂 Birthday party supplies",
        ]
        
        for item_text in placeholder_items:
            item_btn = QPushButton(item_text)
            item_btn.setObjectName("history_item")
            item_btn.setCursor(Qt.PointingHandCursor)
            item_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 12px;
                    color: {CURRENT_THEME.TEXT_SECONDARY};
                    text-align: left;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {CURRENT_THEME.BG_SIDEBAR_HOVER};
                    color: {CURRENT_THEME.TEXT_PRIMARY};
                }}
            """)
            history_layout.addWidget(item_btn)
        
        history_layout.addStretch()
        history_scroll.setWidget(history_content)
        layout.addWidget(history_scroll, 1)
        
        return sidebar
        
    def _create_chat_area(self):
        """Create the center chat area"""
        container = QWidget()
        container.setObjectName("chat_container")
        container.setStyleSheet(f"background-color: {CURRENT_THEME.BG_MAIN};")
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Get the chat widget from presenter
        chat_widget = self.chat_presenter.get_widget()
        layout.addWidget(chat_widget)
        
        return container
        
    def _create_cart_panel(self):
        """Create the right cart panel"""
        container = QWidget()
        container.setObjectName("cart_container")
        container.setFixedWidth(340)
        container.setStyleSheet(f"""
            #cart_container {{
                background-color: {CURRENT_THEME.BG_SIDEBAR};
                border-left: 1px solid {CURRENT_THEME.BORDER_SUBTLE};
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Get the cart widget from presenter
        cart_widget = self.cart_presenter.get_widget()
        layout.addWidget(cart_widget)
        
        return container

    def toggle_sidebar(self):
        """Animate sidebar collapse/expand"""
        if self.sidebar_animation and self.sidebar_animation.state() == QPropertyAnimation.Running:
            return  # Don't interrupt ongoing animation
            
        self.sidebar_animation = QPropertyAnimation(self.sidebar_container, b"maximumWidth")
        self.sidebar_animation.setDuration(200)
        self.sidebar_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        if self.sidebar_expanded:
            # Collapse
            self.sidebar_animation.setStartValue(260)
            self.sidebar_animation.setEndValue(0)
            self.sidebar_expanded = False
        else:
            # Expand
            self.sidebar_container.show()
            self.sidebar_animation.setStartValue(0)
            self.sidebar_animation.setEndValue(260)
            self.sidebar_expanded = True
            
        self.sidebar_animation.start()

    # ============= Interaction Handlers ====================================================================
    def handle_cart_update(self, item_id, new_quantity):
        print(f"Controller: Syncing item {item_id} to quantity {new_quantity}")
        
        # Create and start the background worker
        self.update_worker = CartUpdateWorker(self.repo, item_id, new_quantity)
        
        # Connect the worker's finished signal to an inline update function
        self.update_worker.finished.connect(self.on_cart_updated)
        self.update_worker.start()
        
    def on_cart_updated(self, fresh_cart: StoreResult):
        # This gets called automatically when the background DB update finishes
        print("Controller: Cart updated from DB. Refreshing UI...")
        self.cart_presenter.update_data(fresh_cart)
        
    def handle_user_message(self, text):
        """The central function managing the process"""
        
        print(f"[1] USER INPUT: '{text}' received by Controller.")
        
        # 1. Update chat that agent received the request
        self.chat_presenter.display_agent_response("Thinking...")
        
        # 2. Start background worker to call the AI API
        current_user_id = self.user_manager.current_user.id
        
        # Create worker
        self.worker = AIWorker(self.repo, text, current_user_id)
        
        # Connect signals
        self.worker.finished.connect(self.on_ai_response)
        self.worker.start()

    def on_ai_response(self, result):
        """Handling the response from the server/mock"""
        
        if isinstance(result, str):

            print(f"[5] CONTROLLER: Agent text received: '{result}'")
            self.chat_presenter.display_agent_response(result)
            
            print(f"[6] CONTROLLER: Triggering Cart Refresh (fetch_cart)...")
            cart_data = self.repo.fetch_cart()
            
            print(f"[8] CONTROLLER: Updating UI with {len(cart_data.items)} items.")
            self.cart_presenter.update_data(cart_data)

    def handle_optimize_request(self):
        """Called when user clicks 'Find Cheapest Store'"""
        print("Controller: Optimizing cart requested...")
        self.chat_presenter.display_agent_response("🔄 Checking prices across all stores...")
        
        # Start the background worker
        self.opt_worker = CartOptimizeWorker(self.repo)
        
        # Reuse on_cart_updated because it does exactly what we need (updates the UI)
        self.opt_worker.finished.connect(self.on_optimize_finished)
        self.opt_worker.start()
    
    def on_optimize_finished(self, result: StoreResult):
        
        print(f"Controller: Optimization done. Store: {result.store_name}, Total: {result.total_price}")
        self.cart_presenter.update_data(result)
    
        if result.total_price > 0:
            msg = f"✅ Done! The best deal is at **{result.store_name}** for **{result.total_price:.2f} NIS**."
        else:
            msg = "⚠️ Optimization complete, but the cart seems empty or an error occurred."
            
        self.chat_presenter.display_agent_response(msg)