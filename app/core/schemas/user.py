from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    user_email: str
    social_engineering_score: int = 0
    bec_and_quishing_score: int = 0
    email_web_score: int = 0
    auth_score: int = 0
    ssrf_score: int = 0
    endless_score: int = 0
    team_id: Optional[uuid.UUID] = None
    department: Optional[str] = None
    last_updated: datetime = datetime.now()


class UserCreate(UserBase):
    pass


class UserInDB(UserBase):
    user_id: int
