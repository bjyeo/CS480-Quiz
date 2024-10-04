from pydantic import BaseModel
from typing import List

class QuizBase(BaseModel):
    category: str
    sub: str
    question_text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_answer: List[str]