from PySide6.QtCore import QObject
from core.user_manager import UserManager
from .view import UserSettingsView

class UserPresenter(QObject):
    def __init__(self, user_manager: UserManager):
        super().__init__()
        self.manager = user_manager
        self.view = UserSettingsView()
        
        # 1. Connect View -> Manager
        self.view.save_clicked.connect(self.manager.update_full_profile)
        
        # 2. Connect Manager -> Presenter (for refresh loops)
        self.manager.profile_updated.connect(self.on_user_updated)
        
        # 3. Initial Load if user exists
        if self.manager.current_user:
            self.on_user_updated(self.manager.current_user)

    def get_widget(self):
        return self.view

    def on_user_updated(self, user_profile):
        """Distribute the domain object into the view fields"""
        self.view.load_data(
            username=user_profile.username,
            email=user_profile.email,
            address=user_profile.settings.default_address,
            radius=user_profile.settings.radius_km,
            is_kosher=user_profile.settings.is_kosher_only
        )
