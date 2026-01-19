import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator

# --- Value Objects ---

class SearchSettings(BaseModel):
    """User search settings"""
    default_address: str = Field(default="Tel Aviv")
    radius_km: int = Field(default=5)
    is_kosher_only: bool = False
    
    @validator('radius_km')
    def radius_must_be_reasonable(cls, v):
        if v > 100:
            raise ValueError('We don\'t deliver to the moon, calm down with the radius')
        return v

class ChatMessage(BaseModel):
    """Single message entity"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str # "user" or "agent"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

# --- Aggregate Root ---

class UserProfile(BaseModel):
    """The complete user aggregate"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: Optional[EmailStr] = None
    
    settings: SearchSettings = Field(default_factory=SearchSettings)
    chat_history: List[ChatMessage] = Field(default_factory=list)

    def add_message(self, role: str, content: str):
        """Appends message and enforces constraints"""
        new_msg = ChatMessage(role=role, content=content)
        self.chat_history.append(new_msg)
        
        # Enforce history limit
        if len(self.chat_history) > 50:
            self.chat_history.pop(0)