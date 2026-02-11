import requests
import json
from models.types import AgentResponse, ClarificationRequest, CartItem

class SupermarketAPIClient:
    def __init__(self, agent_url="http://localhost:8000/chat_message", database_url="http://localhost:8001"):
        self.agent_url = agent_url
        self.database_url = database_url

    def search_products(self, prompt: str, user_id: str) -> dict:
        url = f"{self.agent_url}"
        payload = {"message": prompt}
        
        try:
            response = requests.post(self.agent_url, json=payload)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            raise Exception("No connection to server")
        except Exception as e:
            raise Exception(f"API Error: {e}")
    
    def update_cart_item(self, user_id: str, item_name: str, quantity: int):
        url = f"{self.database_url}/create_cart"
        payload = {
            "action": "remove",
            "item": [item_name],
            "quantities": [quantity],
        }
        requests.post(url, json=payload)