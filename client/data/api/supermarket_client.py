import requests
import json
from models.types import StoreResult, ClarificationRequest, CartItem

class SupermarketAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def search_products(self, prompt: str, user_id: str) -> dict:
        url = f"{self.base_url}/api/search"
        payload = {
            "prompt": prompt,
            "user_id": user_id
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            raise Exception("No connection to server")
        except Exception as e:
            raise Exception(f"API Error: {e}")