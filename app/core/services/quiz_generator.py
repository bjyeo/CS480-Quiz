import random
from typing import List
from app.core.schemas.quiz import QuizBase
from app.core.services.supabase import supabase_client


def generate_quiz(subcategory: str) -> List[QuizBase]:
    response = (
        supabase_client.table("quizzes").select(
            "*").eq("sub", subcategory).execute()
    )
    all_questions = response.data

    if len(all_questions) < 15:
        raise ValueError(f"Not enough questions in subcategory {subcategory}")

    selected_questions = random.sample(all_questions, 15)
    return [QuizBase(**q) for q in selected_questions]
