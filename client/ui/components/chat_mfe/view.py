from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

class ChatView(QWidget):
    # Defining events that the View can emit to the Presenter
    send_clicked = Signal(str) 

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)
        
        # Section title
        title_label = QLabel("AI Shopping Assistant")
        title_label.setObjectName("SectionTitle")
        
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setObjectName("ChatHistory")
        
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("What do you need? (e.g., 'milk, eggs, bread for the week')")
        self.input_field.setMaximumHeight(90)
        self.input_field.setMinimumHeight(60)
        
        self.send_btn = QPushButton("Send Request")
        self.send_btn.setObjectName("PrimaryActionBtn")
        self.send_btn.setCursor(Qt.PointingHandCursor)
        
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
            self.send_clicked.emit(text) # Emit to Presenter
            self.input_field.clear()

    # Functions that the Presenter will call to update the screen
    def append_message(self, sender, text):
        # Premium message styling with proper colors from theme
        if sender == "Me":
            sender_color = "#6366f1"  # Electric Indigo
            display_name = "YOU"
        else:
            sender_color = "#10b981"  # Success Green
            display_name = "AGENT"
        
        self.history_display.append(
            f"<div style='margin-bottom: 12px; padding: 8px;'>"
            f"<span style='color:{sender_color}; font-weight:700; font-size:12px; letter-spacing:0.5px;'>{display_name}</span><br>"
            f"<span style='color:#fafafa; line-height:1.6;'>{text}</span>"
            f"</div>"
        )