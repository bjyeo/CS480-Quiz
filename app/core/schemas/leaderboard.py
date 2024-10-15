from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    user_email: EmailStr
    team_id: Optional[UUID]
    department: Optional[str]
    leaderboard_score: int
    last_updated: datetime

class TeamLeaderboardEntry(BaseModel):
    rank: int
    team_id: UUID
    team_name: str
    average_score: float

class ScoreUpdate(BaseModel):
    user_email: EmailStr
    score: int