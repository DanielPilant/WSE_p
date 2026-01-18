from PySide6.QtCore import QThread, Signal

class AIWorker(QThread):
    # Signal that can pass any type of object (Cart or Question)
    finished = Signal(object) 

    def __init__(self, repository, user_prompt):
        super().__init__()
        self.repository = repository
        self.prompt = user_prompt

    def run(self):
        # The heavy operation runs here, in the background
        result = self.repository.send_prompt_to_ai(self.prompt)
        self.finished.emit(result)