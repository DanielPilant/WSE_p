from PySide6.QtCore import QObject, Signal

from ui.components.chat_mfe.view import ChatView
from .model import ChatModel

class ChatPresenter(QObject):
    # Signal emitted from this entire MFE to the AppController
    user_input_submitted = Signal(str)

    def __init__(self):
        super().__init__()
        # 1. Create the internal MVC
        self.view = ChatView()
        self.model = ChatModel()

        # 2. Listen to the View
        self.view.send_clicked.connect(self.handle_send_click)

    def get_widget(self):
        """Function that returns the graphical widget so we can place it in the main window"""
        return self.view

    def handle_send_click(self, text):
        # Update the internal model
        self.model.add_message("Me", text)
        
        # Update the View
        self.view.append_message("Me", text)
        
        # Pass the info to AppController (which will talk to the AI)
        self.user_input_submitted.emit(text)

    def display_agent_response(self, text):
        """Function that the AppController will call from outside"""
        self.model.add_message("Agent", text)
        self.view.append_message("Agent", text)