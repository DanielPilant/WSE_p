from PySide6.QtCore import QThread, Signal, QRunnable

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
        
class CartUpdateWorker(QRunnable):
    def __init__(self, repo, item_id, quantity):
        super().__init__()
        self.repo = repo
        self.item_id = item_id
        self.quantity = quantity

    def run(self):
        try:
            self.repo.update_cart_item(self.item_id, self.quantity)
        except Exception as e:
            print(f"Background update failed: {e}")