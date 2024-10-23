from fastapi import APIRouter, HTTPException
from typing import List
from app.core.schemas.leaderboard import (
    IndividualLeaderboardEntry,
    TeamLeaderboardEntry,
    DepartmentLeaderboardEntry
)
from app.core.services.leaderboard_service import (
    get_top_individual_players,
    get_individual_player_rank,
    get_top_teams,
    get_top_departments,
    update_player_score
)

router = APIRouter()

# Individual leaderboard routes


@router.get("/leaderboard/individual/top", response_model=List[IndividualLeaderboardEntry])
async def get_top_individuals(limit: int = 10):
    try:
        response = await get_top_individual_players(limit)
        players = response.data if response.data else []
        for idx, player in enumerate(players, 1):
            player['rank'] = idx
        return players
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/leaderboard/individual/player/{user_email}", response_model=IndividualLeaderboardEntry)
async def get_individual_ranking(user_email: str):
    try:
        response = await get_individual_player_rank(user_email)
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Player not found")
        return response.data[0]
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/leaderboard/individual/score/{user_id}")
async def update_individual_score(user_id: int, new_score: int):
    try:
        response = await update_player_score(user_id, new_score)
        if not response:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Score updated successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Team leaderboard routes


@router.get("/leaderboard/team/top", response_model=List[TeamLeaderboardEntry])
async def get_top_team_rankings(limit: int = 10):
    try:
        response = await get_top_teams(limit)
        return response.data if response.data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Department leaderboard routes


@router.get("/leaderboard/department/top", response_model=List[DepartmentLeaderboardEntry])
async def get_top_department_rankings(limit: int = 10):
    try:
        response = await get_top_departments(limit)
        return response.data if response.data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

