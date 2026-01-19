import time
from models.user_models import UserProfile

class UserAPIClient:
    """
    Simulates a REST Client implementation.
    """
    def login(self, username: str) -> UserProfile:
        print(f"[API] POST /auth/login payload={{'username': '{username}'}}")
        # Simulate Network Delay
        time.sleep(0.5)
        
        # Return a fresh profile from "Database"
        return UserProfile(
            username=username, 
            email=f"{username.lower()}@example.com"
        )

    def sync_profile(self, profile: UserProfile):
        print(f"[API] PUT /users/{profile.id}")
        time.sleep(0.2)
        # In a real app, this would serialize to JSON
        print(f"[API] Body: {profile.model_dump_json(indent=2)}")
