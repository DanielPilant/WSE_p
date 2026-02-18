from PySide6.QtCore import QThread, Signal, QRunnable
from models.types import StoreResult

class AIWorker(QThread):
    finished = Signal(object) 

    def __init__(self, repository, user_prompt, user_id):
        super().__init__()
        self.repository = repository
        self.prompt = user_prompt
        self.user_id = user_id  

    def run(self):
        result = self.repository.send_prompt_to_ai(self.prompt, self.user_id)
        self.finished.emit(result)
        
class CartUpdateWorker(QThread):
    # This signal will carry the updated StoreResult back to the Controller
    finished = Signal(StoreResult)

    def __init__(self, repository, item_id, new_quantity):
        super().__init__()
        self.repository = repository
        self.item_id = item_id
        self.new_quantity = new_quantity

    def run(self):
        # Runs the heavy 3-step pipeline in the background
        updated_cart = self.repository.update_cart_item(self.item_id, self.new_quantity)
        
        # Send the final result back to the main thread
        self.finished.emit(updated_cart)
    
class CartOptimizeWorker(QThread):
    # Returns the new optimized cart
    finished = Signal(StoreResult)

    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def run(self):
        # Runs the optimization in background
        optimized_cart = self.repository.optimize_current_cart()
        self.finished.emit(optimized_cart)