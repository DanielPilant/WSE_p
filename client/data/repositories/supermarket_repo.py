from models.types import AgentResponse, ClarificationRequest, CartItem
from data.api.supermarket_client import SupermarketAPIClient

class SupermarketRepository:
    def __init__(self):
        self.api = SupermarketAPIClient() # Connection to the API layer

    def send_prompt_to_ai(self, user_text: str, user_id: str):
        # 1. Call to server
        try:
            raw_response = self.api.search_products(user_text, user_id)
            
            # 2. Response parsing (Factory Pattern)
            msg_type = raw_response.get("type")
            data = raw_response.get("data")

            if msg_type == "response":
                # Convert from Dict to AgentResponse object
                # We also need to convert the inner list of items!
                # items_objs = [CartItem(**item) for item in data["items"]]
                
                return AgentResponse(
                    ai_message=data["ai_message"],
                )

            # elif msg_type == "clarification":
            #     return ClarificationRequest(
            #         question=data["question"],
            #         options=data["options"]
            #     )
            
            else:
                raise ValueError("Unknown response type from server")

        except Exception as e:
            # In case of error, return an error message to the user (e.g. via the Clarification mechanism)
            # Or raise an Exception that the Worker will catch
            print(f"Repository Error: {e}")
            return ClarificationRequest(question="Server Error", options=["Try Again"])
        
    def update_cart_item(self, item_name: str, quantity: int):
        """
        Sends the quantity update to the API Client.
        """
        self.api.update_cart_item("dummy_user_id", item_name, quantity)