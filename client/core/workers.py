from PySide6.QtCore import QThread, Signal

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