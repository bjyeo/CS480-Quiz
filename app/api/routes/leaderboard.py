from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.schemas.leaderboard import LeaderboardEntry, TeamLeaderboardEntry, ScoreUpdate
from app.core.services.leaderboard_service import LeaderboardService
from app.core.services.supabase import supabase_client

router = APIRouter()

def get_leaderboard_service():
    return LeaderboardService(supabase_client)

@router.post("/leaderboards/update-score", response_model=LeaderboardEntry)
def update_score(score_update: ScoreUpdate, service: LeaderboardService = Depends(get_leaderboard_service)):
    return service.update_score(score_update)

@router.get("/leaderboards/top-players", response_model=List[LeaderboardEntry])
def get_top_players(limit: int = 10, service: LeaderboardService = Depends(get_leaderboard_service)):
    return service.get_top_users(limit)

@router.get("/leaderboards/player-position", response_model=LeaderboardEntry)
def get_player_position(email: str, service: LeaderboardService = Depends(get_leaderboard_service)):
    position = service.get_user_position(email)
    if position is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return position

@router.get("/leaderboards/department-position", response_model=LeaderboardEntry)
def get_department_position(email: str, department: str, service: LeaderboardService = Depends(get_leaderboard_service)):
    position = service.get_department_position(email, department)
    if position is None:
        raise HTTPException(status_code=404, detail="Player not found in department")
    return position

@router.get("/leaderboards/team-position", response_model=TeamLeaderboardEntry)
def get_team_position(team_id: str, service: LeaderboardService = Depends(get_leaderboard_service)):
    position = service.get_team_position(team_id)
    if position is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return position