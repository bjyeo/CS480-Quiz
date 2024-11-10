from app.core.services.supabase import supabase_client
from fastapi import HTTPException


async def get_top_individual_players(limit: int = 10):
    return supabase_client.from_("individual_leaderboard")\
        .select("*")\
        .limit(limit)\
        .execute()


async def get_individual_player_rank(user_email: str):
    try:
        response = supabase_client.from_("individual_leaderboard")\
            .select("*")\
            .eq("user_email", user_email)\
            .execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Player not found")
        return response
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_top_teams(limit: int = 10):
    return supabase_client.from_("team_leaderboard")\
        .select("*")\
        .limit(limit)\
        .execute()


async def get_top_departments(limit: int = 10):
    return supabase_client.from_("department_leaderboard")\
        .select("*")\
        .limit(limit)\
        .execute()


async def update_player_score(user_id: int, new_score: int):
    try:
        response = supabase_client.from_("users").update(
            {"endless_score": new_score}
        ).eq("user_id", user_id).execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")

        # If user exists, proceed with update
        response = supabase_client.from_("users")\
            .update({"endless_score": new_score})\
            .eq("user_id", user_id)\
            .execute()

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
