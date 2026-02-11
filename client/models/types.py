from dataclasses import dataclass
from typing import List, Optional

# Representation of an item in the cart
@dataclass
class CartItem:
    id: str
    name: str
    quantity: int
    price: float

# Representation of a successful response from the server
@dataclass
class AgentResponse:
    ai_message: str

# Representation of a clarification request (when the AI is confused)
@dataclass
class ClarificationRequest:
    question: str
    options: List[str]