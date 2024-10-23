from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    user_email: str
    endless_score: int
