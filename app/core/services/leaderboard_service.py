from app.core.services.supabase import supabase_client
from fastapi import HTTPException
# from typing import Optional


async def get_top_players(limit: int = 10):
    return supabase_client.from_("users").select("*").order('endless_score', desc=True).limit(limit).execute()


async def get_player_rank(user_email: str):
    try:
        all_players = supabase_client.from_("users").select(
            "*").order('endless_score', desc=True).execute()

        for idx, player in enumerate(all_players.data, 1):
            if player['user_email'] == user_email:
                player['rank'] = idx
                return type('Response', (), {'data': player})()

        raise HTTPException(status_code=404, detail="Player not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_player_score(user_id: int, new_score: int):
    try:
        response = supabase_client.from_("users").update(
            {"endless_score": new_score}
        ).eq("user_id", user_id).execute()

        if not response.data:
            return None
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
