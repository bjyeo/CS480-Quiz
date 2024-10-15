from fastapi import FastAPI
from app.api.routes import quiz
from app.api.routes import leaderboard
import uvicorn

app = FastAPI(title="Quiz API")

app.include_router(quiz.router, prefix="/api/v1", tags=["quizzes"])
app.include_router(leaderboard.router, prefix="/api/v1", tags=["leaderboard"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Quiz API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
