from fastapi import APIRouter, HTTPException
from typing import List
from app.core.schemas.quiz import Quiz
from app.core.services.supabase import supabase_client

router = APIRouter()

@router.get("/quizzes/", response_model=List[Quiz])
async def get_all_quiz_questions():
    try:
        response = supabase_client.table("quizzes").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/quizzes/subcategory/{sub}", response_model=List[Quiz])
async def get_questions_by_subcategory(sub: str):
    try:
        response = supabase_client.table("quizzes").select("*").eq("sub", sub).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No questions found for subcategory: {sub}")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")