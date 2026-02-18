from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Signal

class ChatView(QWidget):
    send_clicked = Signal(str) 

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)
        
        title_label = QLabel("AI Shopping Assistant")
        
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("What do you need? (e.g., 'milk, eggs, bread for the week')")
        self.input_field.setMaximumHeight(90)
        self.input_field.setMinimumHeight(60)
        
        self.send_btn = QPushButton("Send Request")
        
        self.layout.addWidget(title_label)
        self.layout.addWidget(self.history_display, 8)
        self.layout.addWidget(self.input_field, 1)
        self.layout.addWidget(self.send_btn)
        
        self.setLayout(self.layout)
        
        # Internal connection: button click -> call helper function that emits signal
        self.send_btn.clicked.connect(self._on_send_btn)

    def _on_send_btn(self):
        text = self.input_field.toPlainText().strip()
        if text:
            self.send_clicked.emit(text)
            self.input_field.clear()

    def append_message(self, sender, text):
        self.history_display.append(f"[{sender}]: {text}")