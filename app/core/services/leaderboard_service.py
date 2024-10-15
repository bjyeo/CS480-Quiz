from app.core.schemas.leaderboard import LeaderboardEntry, TeamLeaderboardEntry, ScoreUpdate
from typing import List, Optional
from uuid import UUID

class LeaderboardService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def update_score(self, score_update: ScoreUpdate) -> LeaderboardEntry:
        self.supabase.rpc("update_endless_score", {
            "p_user_email": score_update.user_email,
            "p_score": score_update.score
        }).execute()
        return self.get_user_position(score_update.user_email)

    def get_top_users(self, limit: int = 10) -> List[LeaderboardEntry]:
        response = (self.supabase.table("leaderboard")
                    .select("*")
                    .limit(limit)
                    .execute())
        return [LeaderboardEntry(**entry) for entry in response.data]

    def get_user_position(self, email: str) -> Optional[LeaderboardEntry]:
        rank = self.supabase.rpc("get_user_rank", {"p_user_email": email}).execute()
        if rank.data:
            user = self.supabase.table("leaderboard").select("*").eq("user_email", email).single().execute()
            return LeaderboardEntry(rank=rank.data[0]['get_user_rank'], **user.data)
        return None

    def get_department_position(self, email: str, department: str) -> Optional[LeaderboardEntry]:
        rank = self.supabase.rpc("get_user_department_rank", {
            "p_user_email": email,
            "p_department": department
        }).execute()
        if rank.data:
            user = self.supabase.table("leaderboard").select("*").eq("user_email", email).single().execute()
            return LeaderboardEntry(rank=rank.data[0]['get_user_department_rank'], **user.data)
        return None

    def get_team_position(self, team_id: UUID) -> Optional[TeamLeaderboardEntry]:
        rank = self.supabase.rpc("get_team_rank", {"p_team_id": str(team_id)}).execute()
        if rank.data:
            team_data = self.supabase.table("users").select("team_id", "AVG(endless_score) as average_score").eq("team_id", str(team_id)).group_by("team_id").single().execute()
            return TeamLeaderboardEntry(
                rank=rank.data[0]['get_team_rank'],
                team_id=team_id,
                team_name="Team Name",  # You might need to fetch this from a teams table if you have one
                average_score=team_data.data['average_score']
            )
        return None