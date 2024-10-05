from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict
from app.core.schemas.quiz import QuizBase, QuizQuestion, QuizSubmission
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
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/quizzes/category/{sub}", response_model=List[QuizBase])
async def get_questions_by_subcategory(sub: str):
    try:
        response = supabase_client.table("quizzes").select("*").eq("sub", sub).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No questions found for subcategory: {sub}")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/generate-quiz/{subcategory}", response_model=List[QuizQuestion])
async def generate_user_quiz(subcategory: str, user_id: int = Query(...)):
    try:
        user_response = supabase_client.table("users").select("user_id").eq("user_id", user_id).execute()
        if not user_response.data:
            raise HTTPException(status_code=404, detail="User not found")

        quiz = generate_quiz(subcategory, user_id)
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/submit-quiz/{subcategory}", response_model=Dict[str, int])
async def submit_quiz(subcategory: str, user_id: int = Query(...), submission: QuizSubmission = Body(...)):
    try:
        correct_quiz = generate_quiz(subcategory, user_id)
        
        new_score = sum(1 for submitted, correct in zip(submission.answers, correct_quiz) 
                        if submitted == correct.correct_answer)
        
        user_response = supabase_client.table("users").select(f"{subcategory}_score").eq("user_id", user_id).execute()
        if not user_response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_score = user_response.data[0].get(f"{subcategory}_score", 0)
        
        if new_score > current_score:
            supabase_client.table("users").update({f"{subcategory}_score": new_score}).eq("user_id", user_id).execute()
            return {"score": new_score, "improved": True}
        else:
            return {"score": new_score, "improved": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")