from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from ui.components.cart_mfe.presenter import CartPresenter
from ui.components.chat_mfe.presenter import ChatPresenter
from ui.components.user_mfe.presenter import UserPresenter
from data.repositories.supermarket_repo import SupermarketRepository
from ui.dialogs.ambiguity_dialog import AmbiguityDialog
from core.workers import AIWorker
from core.user_manager import UserManager
from models.types import ClarificationRequest, StoreResult

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supermarket Agent - Final Project")
        self.resize(1400, 700)
        
        # --- Data & State Layer ---
        self.repo = SupermarketRepository()
        self.user_manager = UserManager()
        
        # --- Presentation Layer ---
        # We create the "brains", they will create their UI internally
        self.user_presenter = UserPresenter(self.user_manager)
        self.chat_presenter = ChatPresenter()
        self.cart_presenter = CartPresenter()
        
        # --- Main UI Layout ---
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Pulling the graphic widgets from the presenters
        main_layout.addWidget(self.user_presenter.get_widget(), 20) # 20% width
        main_layout.addWidget(self.chat_presenter.get_widget(), 40) # 40% width
        main_layout.addWidget(self.cart_presenter.get_widget(), 40) # 40% width
        
        self.setCentralWidget(central_widget)
        
        # --- Wiring / Logic Flow ---
        # When user sends a message in chat -> trigger the main function in Controller
        self.chat_presenter.user_input_submitted.connect(self.handle_user_message)
        
        # --- Bootstrap ---
        self.user_manager.login_guest()

    def handle_user_message(self, text):
        """The central function managing the process"""
        
        # 1. Update chat that agent received the request
        self.chat_presenter.display_agent_response("Checking supermarkets...")
        
        # 2. Start background worker to call the AI API
        current_user_id = self.user_manager.current_user.id
        
        # Create worker
        self.worker = AIWorker(self.repo, text, current_user_id)
        
        # Connect signals
        self.worker.finished.connect(self.on_ai_response)
        self.worker.start()

    def on_ai_response(self, result):
        """Handling the response from the server/mock"""
        
        # --- Case A: Server is confused (Clarification) ---
        if isinstance(result, ClarificationRequest):
            # Create modal dialog
            dialog = AmbiguityDialog(result, self)
            if dialog.exec(): 
                # If user chose an option and clicked OK
                choice = dialog.selected_choice
                self.chat_presenter.display_agent_response(f"Great, you chose: {choice}")
                
                # Logic recursion: sending choice back to engine
                self.handle_user_message(f"User specifically chose: {choice}")

        # --- Case B: Server returned a result (StoreResult) ---
        elif isinstance(result, StoreResult):
            # Update Chat
            self.chat_presenter.display_agent_response(
                f"Found it! The cheapest basket is at {result.store_name}."
            )
            # Update Cart Micro-Frontend with new data
            self.cart_presenter.update_data(result)