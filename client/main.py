import sys
import os
from PySide6.QtWidgets import QApplication
from core.app_controller import AppController

def load_stylesheet(app):
    
    file_path = os.path.join("ui", "styles", "global.qss")
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            print("Stylesheet loaded successfully.")
    else:
        print(f"Warning: Stylesheet not found at {file_path}")


if __name__ == "__main__":
    # Create the application (global resource management)
    app = QApplication(sys.argv)
    
    # Load the global stylesheet
    load_stylesheet(app)
    
    # Create the main controller
    controller = AppController()
    controller.show()
    
    # Start the event loop (Event Loop)
    # This is not a REPL, the software "hangs" here waiting for mouse clicks
    sys.exit(app.exec())