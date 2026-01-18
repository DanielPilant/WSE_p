from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from models.types import ClarificationRequest

class AmbiguityDialog(QDialog):
    def __init__(self, request: ClarificationRequest, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clarification Needed")
        self.selected_choice = None
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(request.question))
        
        # Dynamic creation of buttons based on options received from the server
        for option in request.options:
            btn = QPushButton(option)
            # Using lambda to know which button was clicked
            btn.clicked.connect(lambda checked, opt=option: self.on_choice(opt))
            layout.addWidget(btn)
            
        self.setLayout(layout)

    def on_choice(self, option):
        self.selected_choice = option
        self.accept() # Closes the dialog successfully (Result Code = Accepted)