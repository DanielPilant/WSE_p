from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import QThreadPool
from ui.components.cart_mfe.presenter import CartPresenter
from ui.components.chat_mfe.presenter import ChatPresenter
from ui.components.user_mfe.presenter import UserPresenter
from data.repositories.supermarket_repo import SupermarketRepository
from ui.dialogs.ambiguity_dialog import AmbiguityDialog
from core.workers import AIWorker, CartUpdateWorker
from core.user_manager import UserManager
from models.types import ClarificationRequest, StoreResult

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supermarket Agent - Final Project")
        self.resize(1000, 700)
        
        # --- Data & State Layer ---
        self.repo = SupermarketRepository()
        self.user_manager = UserManager()
        
        # --- Presentation Layer ---
        # We create the "brains", they will create their UI internally
        self.chat_presenter = ChatPresenter()
        self.cart_presenter = CartPresenter(self.repo) # We pass the repo to the Cart Presenter so it can update the server when user changes quantity
        
        # Connect cart item change signal to update worker
        self.cart_presenter.cart_item_changed.connect(self.handle_cart_update)
        
        # --- Main UI Layout ---
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Pulling the graphic widgets from the presenters
        main_layout.addWidget(self.chat_presenter.get_widget(), 40) # 40% width
        main_layout.addWidget(self.cart_presenter.get_widget(), 40) # 40% width
        
        self.setCentralWidget(central_widget)
        
        # --- Wiring / Logic Flow ---
        # When user sends a message in chat -> trigger the main function in Controller
        self.chat_presenter.user_input_submitted.connect(self.handle_user_message)
        
        # --- Bootstrap ---
        self.user_manager.login_guest()
        
        print("Initializing session with Agent...")
        is_connected = self.repo.initialize_session()
        
        if not is_connected:
            self.chat_presenter.display_agent_response("⚠️ Warning: Could not connect to the Agent server. Is it running on port 8001?")
        else:
            self.chat_presenter.display_agent_response("Hi! The system is ready. What would you like to add to your cart?")

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
