from typing import List, Optional
from models.types import CartItem, StoreResult

class CartModel:
    def __init__(self):
        # Initial State
        self.store_name: str = ""
        self.store_address: str = ""
        self.total_price: float = 0.0
        self.items: List[CartItem] = []

    def set_data(self, store_result: StoreResult):
        """Update all data at once (e.g. when AI returns a result)"""
        self.store_name = store_result.store_name
        self.store_address = store_result.address
        self.total_price = store_result.total_price
        self.items = store_result.items

    def update_quantity(self, item_id: str, delta: int):
        """Business logic: change quantity and update total price"""
        for item in self.items:
            if item.id == item_id:
                # Update quantity (prevent going below 0)
                if item.quantity + delta >= 0:
                    item.quantity += delta
                    # Update total price accordingly
                    self.total_price += (item.price * delta)
                    return True
        return False
    
    def get_item_quantity(self, item_id: str) -> Optional[int]:
        """Helper function to get current quantity of an item (for syncing with server)"""
        for item in self.items:
            if item.id == item_id:
                return item.quantity
        return None