from pydantic import BaseModel
from typing import Optional
import uuid


class IndividualLeaderboardEntry(BaseModel):
    rank: int
    user_email: str
    endless_score: int
    team_id: Optional[uuid.UUID] = None
    department: Optional[str] = None


class TeamLeaderboardEntry(BaseModel):
    rank: int
    team_id: uuid.UUID
    total_score: int


class DepartmentLeaderboardEntry(BaseModel):
    rank: int
    department: str
    total_score: int
