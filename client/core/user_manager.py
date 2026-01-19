from PySide6.QtCore import QObject, Signal
from models.user_models import UserProfile, SearchSettings
from data.api.user_client import UserAPIClient

# Domain Layer: Manages User State and Synchronization with Backend
class UserManager(QObject):
    
    # Signal emitted when user profile is updated. ChatMFE, CartMFE, etc. can listen to this.
    profile_updated = Signal(UserProfile)

    def __init__(self):
        super().__init__()
        self.client = UserAPIClient()
        self.current_user = None # single source of truth

    def login_guest(self):
        """Bootstraps the application with a default user"""
        # In blocking mode for simplicity (Use Threads in production)
        self.current_user = self.client.login("GuestUser")
        self.profile_updated.emit(self.current_user)

    def update_full_profile(self, data_dict: dict):
        """
        Receives raw dictionary from UI, updates the Domain Model, 
        and syncs with Backend.
        """
        if not self.current_user:
            return

        # 1. Update Root Fields using Pydantic's model_copy or direct assignment
        # (Using direct assignment here for readability on mutable instances)
        self.current_user.username = data_dict.get("username", self.current_user.username)
        self.current_user.email = data_dict.get("email", self.current_user.email)

        # 2. Update Nested Settings
        # leveraging Pydantic validation
        new_settings = SearchSettings(
            default_address=data_dict.get("address", ""),
            radius_km=data_dict.get("radius", 5),
            is_kosher_only=data_dict.get("kosher", False)
        )
        self.current_user.settings = new_settings

        # 3. Cloud Sync
        self.client.sync_profile(self.current_user)
        
        # 4. Notify UI components
        self.profile_updated.emit(self.current_user)

    def add_chat_msg(self, role: str, content: str):
        if self.current_user:
            self.current_user.add_message(role, content)
            # Silent sync (fire and forget)
            self.client.sync_profile(self.current_user)
