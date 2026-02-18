from models.types import StoreResult, ClarificationRequest, CartItem
from data.api.supermarket_client import SupermarketAPIClient

class SupermarketRepository:
    def __init__(self):
        self.api = SupermarketAPIClient() # Connection to the API layer
        self.current_cart_id = None

    def send_prompt_to_ai(self, user_text: str, user_id: str):
        # 1. Call to server
        try:
            raw_response = self.api.send_message(user_text, user_id)
            
            print(f"[4] REPO: Agent Raw Response: {raw_response}")
            
            # 2. Response parsing (Factory Pattern)
            msg_type = raw_response.get("type")
            data = raw_response.get("data")

            if msg_type == "response":
                ai_text = data.get("ai_message")
                print(f"Repository: Received AI response: {ai_text}")
                return ai_text
            
            else:
                raise ValueError("Unknown response type from server")

        except Exception as e:
            # In case of error, return an error message to the user (e.g. via the Clarification mechanism)
            # Or raise an Exception that the Worker will catch
            print(f"Repository Error: {e}")
            return ClarificationRequest(question="Server Error", options=["Try Again"])
        
    def initialize_session(self) -> bool:
        try:
            result = self.api.initialize_session()
            message = result.get("data", {}).get("message", "Session started")
            self.current_cart_id = result.get("data", {}).get("cart_id")
            print(f"✅ System Ready: {message}. cart id is {self.current_cart_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize session: {e}")
            return False
    
    def fetch_cart(self) -> StoreResult:
        """Fetches the cart directly from the DB and converts it safely to the frontend model"""
        print(f"[7] REPO: Fetching fresh cart from DB (Port 8000)...")
        
        if not self.current_cart_id:
            print("⚠️ No cart ID stored in Repo. Cannot fetch.")
            return StoreResult("Empty Cart", "", 0.0, [])

        try:
            print(f"Fetching cart from DB with ID: {self.current_cart_id}")
            data = self.api.get_cart_from_db(self.current_cart_id)
            
            # Print the raw DB payload so we can see exactly what came from the backend
            print(f"Raw DB Cart Data: {data}")
            
            cart_data = data.get("cart", {})
            items_list = cart_data.get("items", [])
            
            print(f"[7.5] REPO: DB returned items: {items_list}")
            
            print(f"Found {len(items_list)} items in the DB response.")
            
            items_objs = []
            for idx, item in enumerate(items_list):
                # Safely extract values: Backend might use 'item_name' or 'name'
                item_name = item.get("item_name") or item.get("name") or f"Item {idx}"
                quantity = item.get("quantity", 1)
                price = item.get("price", 0.0)
                
                # Make sure the ID is a string (fallback to item_name if no ID exists)
                item_id = str(item.get("id") or item_name)
                
                items_objs.append(CartItem(
                    id=item_id,
                    name=item_name,
                    quantity=int(quantity),
                    price=float(price)
                ))
            
            # Extract store info safely
            store_name = cart_data.get("store_name") or "Supermarket"
            address = cart_data.get("address") or ""
            total_price = float(cart_data.get("total_price") or 0.0)
            
            result_model = StoreResult(
                store_name=store_name,
                address=address,
                total_price=total_price,
                items=items_objs
            )
            
            print(f"✅ Successfully mapped StoreResult: {len(result_model.items)} items ready for UI")
            return result_model
            
        except Exception as e:
            print(f"❌ Cart Fetch Error: {e}")
            return StoreResult("Server Error", "", 0.0, [])
        
    def update_cart_item(self, item_id: str, new_quantity: int) -> StoreResult:
        """Updates quantity, re-optimizes, and returns the fresh cart"""
        if not self.current_cart_id:
            print("⚠️ Cannot update item: No active cart session.")
            return StoreResult("Error", "", 0.0, [])
            
        try:
            print(f"Step 1: Patching DB Item '{item_id}' to quantity {new_quantity}")
            # 1. Update quantities
            self.api.update_cart_item_in_db(self.current_cart_id, item_id, new_quantity)
            
            print(f"Step 2: Re-optimizing cart {self.current_cart_id}...")
            # 2. Trigger optimization
            self.api.optimize_cart_in_db(self.current_cart_id)
            
            print("Step 3: Fetching fresh cart data...")
            # 3. Pull the updated data using the method we already wrote
            return self.fetch_cart()
            
        except Exception as e:
            print(f"❌ DB Update Pipeline Error: {e}")
            return StoreResult("Update Failed", "", 0.0, [])