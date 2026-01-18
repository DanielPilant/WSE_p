from dataclasses import dataclass

@dataclass
class ChatMessage:
    sender: str  # "User" or "Agent"
    text: str
    timestamp: float = 0.0

class ChatModel:
    def __init__(self):
        self.messages = []

    def add_message(self, sender, text):
        msg = ChatMessage(sender, text)
        self.messages.append(msg)
        return msg