import sys
from PySide6.QtWidgets import QApplication
from core.app_controller import AppController


if __name__ == "__main__":
    # Create the application (global resource management)
    app = QApplication(sys.argv)
    
    # Create the main controller
    controller = AppController()
    controller.show()
    
    # Start the event loop (Event Loop)
    # This is not a REPL, the software "hangs" here waiting for mouse clicks
    sys.exit(app.exec())