import requests
import json
from models.types import StoreResult, ClarificationRequest, CartItem

class SupermarketAPIClient:
    def __init__(self, base_url="http://localhost:8001", db_url="http://localhost:8000"):
        self.base_url = base_url
        self.db_url = db_url

    def send_message(self, prompt: str, user_id: str) -> dict:
        url = f"{self.base_url}/chat_message"
        
        print(f"[2] CLIENT: Sending request to Agent (Port 8001)...")
        
        payload = {
            "message": prompt,
        }
        
        try:
            response = requests.post(url, json=payload, timeout=100)
            response.raise_for_status()
            print(f"[3] CLIENT: Agent responded! Status Code: {response.status_code}")
            return response.json()
            
        except requests.exceptions.ConnectionError:
            raise Exception("No connection to server")
        except Exception as e:
            raise Exception(f"API Error: {e}")
    
    def initialize_session(self) -> dict:
        url = f"{self.base_url}/session/initialize"
        try:
            response = requests.post(url, timeout=100)
            response.raise_for_status()
            print(f"API Client: Session initialization response: {response.text}")
            return response.json()
        except requests.exceptions.ConnectionError:
            print("ERROR: Agent server (8001) is not reachable.")
            raise Exception("No connection to Agent server on port 8001")
        except Exception as e:
            print(f"ERROR: Session initialization failed: {e}")
            raise Exception(f"API Error: {e}")
    
    def get_cart_from_db(self, cart_id: str) -> dict:
        url = f"{self.db_url}/cart/{cart_id}"
        try:
            response = requests.get(url, timeout=100)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"DB API Error (get_cart): {e}")
    
    def update_cart_item_in_db(self, cart_id: str, item_name: str, new_quantity: int) -> dict:
        """Sends a PATCH request to the DB to update an item's quantity"""
        url = f"{self.db_url}/cart/{cart_id}/items"
        payload = {
            "item_names": [item_name],
            "quantities": [new_quantity]
        }
        try:
            response = requests.patch(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"DB API Error (update_items): {e}")
        
    def optimize_cart_in_db(self, cart_id: str) -> dict:
        """Sends a POST request to re-optimize the cart based on current items"""
        url = f"{self.db_url}/cart/{cart_id}/optimize"
        try:
            # Empty POST request as required by the backend
            response = requests.post(url, timeout=60) 
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"DB API Error (optimize): {e}")