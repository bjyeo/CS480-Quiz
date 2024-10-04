import hashlib
import random
from typing import List
from app.core.schemas.quiz import QuizQuestion
from app.core.services.supabase import supabase_client

def generate_quiz(subcategory: str, user_id: int) -> List[QuizQuestion]:
    response = supabase_client.table("quizzes").select("*").eq("sub", subcategory).execute()
    all_questions = response.data

    if len(all_questions) < 15:
        raise ValueError(f"Not enough questions in subcategory {subcategory}")

    hash_input = f"{user_id}_{subcategory}"
    hash_value = hashlib.md5(hash_input.encode()).hexdigest()

    random.seed(hash_value)
    selected_questions = random.sample(all_questions, 15)
    random.shuffle(selected_questions)

    return [QuizQuestion(**q) for q in selected_questions]