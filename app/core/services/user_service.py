from app.core.schemas.user import UserCreate
from app.core.services.supabase import supabase_client


async def get_all_users():
    return supabase_client.table("users").select("*").execute()


async def create_user(user: UserCreate):
    return supabase_client.table("users").insert(user.dict()).execute()


async def get_user(user_id: int):
    return supabase_client.table("users").select("*").eq("user_id", user_id).single().execute()
