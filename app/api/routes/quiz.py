from fastapi import APIRouter, HTTPException
from typing import List
from app.core.schemas.quiz import QuizBase
from app.core.services.supabase import supabase_client
from app.core.services.quiz_generator import generate_quiz

router = APIRouter()


@router.get("/quizzes/", response_model=List[QuizBase])
async def get_all_quiz_questions():
    try:
        response = supabase_client.table("quizzes").select("*").execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="No questions found")
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/quizzes/category/{sub}", response_model=List[QuizBase])
async def get_questions_by_subcategory(sub: str):
    try:
        response = supabase_client.table(
            "quizzes").select("*").eq("sub", sub).execute()
        if not response.data:
            raise HTTPException(
                status_code=404, detail=f"No questions found for subcategory: \
                    {sub}")
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/generate-quiz/{subcategory}", response_model=List[QuizBase])
async def generate_user_quiz(subcategory: str):
    try:
        quiz = generate_quiz(subcategory)
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
