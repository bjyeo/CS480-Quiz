from typing import List
from pydantic import BaseModel

class Quiz(BaseModel):
    id: int
    category: str
    sub: str
    question_text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_answer: List[str]

    class Config:
        from_attributes = True