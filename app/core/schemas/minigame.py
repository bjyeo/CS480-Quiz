from typing import Optional, Dict
from pydantic import BaseModel

class EmailEntry(BaseModel):
    id: int
    from_address: str  # using from_address since 'from' is a Python keyword
    to: str
    subject: str
    content: str

class MinigameResponse(BaseModel):
    email: Dict[str, str]  # Will contain the email fields
    is_modified: bool
    prompt_used: Optional[str] = None  # Will be None if not modified