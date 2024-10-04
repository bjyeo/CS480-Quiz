from pydantic import BaseModel
from typing import List, Optional

class QuizBase(BaseModel):
    category: str
    sub: str
    question_text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_answer: List[str]

class QuizQuestion(BaseModel):
    id: int
    sub: str
    question_text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str

class QuizSubmission(BaseModel):
    answers: List[Optional[List[str]]]