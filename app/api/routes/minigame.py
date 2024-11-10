# api/routes/minigame.py
from fastapi import APIRouter, HTTPException
from app.core.schemas.minigame import MinigameResponse
from app.core.services.minigame_service import get_random_minigame_email
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/minigame", response_model=MinigameResponse)
async def get_minigame_email():
    """
    Retrieves a random email from the minigame_emails table.
    Has a 50% chance of returning the original email or modifying it using GPT-4.
    """
    try:
        return await get_random_minigame_email()
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in minigame endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
