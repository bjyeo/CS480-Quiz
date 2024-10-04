from supabase import create_client, Client
from app.config import settings

supabase_url = settings.SUPABASE_URL
supabase_key = settings.SUPABASE_KEY

supabase_client: Client = create_client(supabase_url, supabase_key)