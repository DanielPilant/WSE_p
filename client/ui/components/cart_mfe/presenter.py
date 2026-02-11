from PySide6.QtCore import QObject, Signal
from .view import CartView
from .model import CartModel
from models.types import AgentResponse

class CartPresenter(QObject):
    
    # Signal emitted when user changes quantity, to notify AppController to update the server
    cart_item_changed = Signal(str, int)
        
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        # 1. Create Model and View
        self.model = CartModel()
        self.view = CartView()
        
        # 2. Listen to events from View (clicks on +/-)
        self.view.item_incremented.connect(self.on_increment)
        self.view.item_decremented.connect(self.on_decrement)

    def get_widget(self):
        """Expose the View to the outside world (for the main Layout)"""
        return self.view

    # def update_data(self, result: StoreResult):
    #     """Function called from outside (by AppController)"""
    #     self.model.set_data(result)
    #     self._refresh_view()
    
    def handle_quantity_change(self, item_id, delta):
        success = self.model.update_quantity(item_id, delta)
        
        if success:
            self._refresh_view()
            current_qty = self.model.get_item_quantity(item_id)
            self.cart_item_changed.emit(item_id, current_qty)
            

    def on_increment(self, item_id):
        self.handle_quantity_change(item_id, +1)

    def on_decrement(self, item_id):
        self.handle_quantity_change(item_id, -1)

    def _refresh_view(self):
        """Takes data from model and pushes it to View"""
        self.view.render_cart(
            self.model.store_name,
            self.model.store_address,
            self.model.items,
            self.model.total_price
        )
    
    