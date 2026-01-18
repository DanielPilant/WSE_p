from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt

class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor)) # Pointing hand
        # Specific logic or styling can be added here if not using global QSS
        self.setMinimumHeight(40)

class DangerButton(PrimaryButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # Specific override for red color
        self.setStyleSheet("background-color: #d50000; color: white;")