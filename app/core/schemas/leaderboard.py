from pydantic import BaseModel
from typing import Optional


class IndividualLeaderboardEntry(BaseModel):
    rank: int
    user_email: str
    endless_score: int
    team_name: Optional[str] = None


class TeamLeaderboardEntry(BaseModel):
    rank: int
    team_name: str
    total_score: int


class DepartmentLeaderboardEntry(BaseModel):
    rank: int
    department: str
    total_score: int
