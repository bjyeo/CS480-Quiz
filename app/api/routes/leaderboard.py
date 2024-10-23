from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.schemas.leaderboard import LeaderboardEntry
from app.core.services.leaderboard_service import (
    get_top_players,
    get_player_rank,
    update_player_score
)

router = APIRouter()


@router.get("/leaderboard/top", response_model=List[LeaderboardEntry])
async def get_leaderboard_top_players(limit: int = 10):
    try:
        response = await get_top_players(limit)
        players = response.data if response.data else []
        # Add rank to each player
        for idx, player in enumerate(players, 1):
            player['rank'] = idx
        return players
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/leaderboard/player/{user_email}", response_model=LeaderboardEntry)
async def get_player_ranking(user_email: str):
    try:
        response = await get_player_rank(user_email)
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return response.data
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/leaderboard/score/{user_id}")
async def update_endless_score(user_id: int, new_score: int):
    try:
        response = await update_player_score(user_id, new_score)
        if not response:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Score updated successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
