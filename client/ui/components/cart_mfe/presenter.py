from PySide6.QtCore import QObject
from .view import CartView
from .model import CartModel
from models.types import StoreResult

class CartPresenter(QObject):
    def __init__(self):
        super().__init__()
        # 1. Create Model and View
        self.model = CartModel()
        self.view = CartView()
        
        # 2. Listen to events from View (clicks on +/-)
        self.view.item_incremented.connect(self.on_increment)
        self.view.item_decremented.connect(self.on_decrement)

    def get_widget(self):
        """Expose the View to the outside world (for the main Layout)"""
        return self.view

    def update_data(self, result: StoreResult):
        """Function called from outside (by AppController)"""
        self.model.set_data(result)
        self._refresh_view()

    def on_increment(self, item_id):
        # Update model
        changed = self.model.update_quantity(item_id, 1)
        if changed:
            self._refresh_view()

    def on_decrement(self, item_id):
        changed = self.model.update_quantity(item_id, -1)
        if changed:
            self._refresh_view()

    def _refresh_view(self):
        """Takes data from model and pushes it to View"""
        self.view.render_cart(
            self.model.store_name,
            self.model.store_address,
            self.model.items,
            self.model.total_price
        )