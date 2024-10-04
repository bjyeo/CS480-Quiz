from fastapi import FastAPI
from app.api.routes import quiz

app = FastAPI(title="Quiz API")

app.include_router(quiz.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Quiz API"}