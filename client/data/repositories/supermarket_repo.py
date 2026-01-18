import time
from models.types import CartItem, StoreResult, ClarificationRequest

class SupermarketRepository:
    """
    This class serves as both DAC and Repository for this stage.
    It simulates REST API communication (Request/Response).
    """
    def send_prompt_to_ai(self, user_text: str):
        # Simulation of network delay (like a real call to the server)
        time.sleep(1.0) 
        
        # Business logic from the AI domain:
        
        # Scenario 1: Ambiguity
        if "bread" in user_text.lower() and "whole" not in user_text.lower():
            return ClarificationRequest(
                question="The agent is deliberating: which bread did you mean?",
                options=["Sliced Standard Bread (4.5 NIS)", "Whole Country Bread (12.90 NIS)", "Sweet Challah (7.50 NIS)"]
            )
            
        # Scenario 2: Success - Returning a full cart
        return StoreResult(
            store_name="Shufersal Deal - Malcha Mall",
            address="1 Agudat Sport Beitar Way",
            total_price=85.50,
            items=[
                CartItem("101", "Tnuva Milk 3%", 2, 6.20),
                CartItem("102", "Eggs L (12 pack)", 1, 14.90),
                CartItem("103", "Telma Cornflakes", 1, 24.50),
                CartItem("104", "Cucumbers (kg)", 2, 4.90)
            ]
        )