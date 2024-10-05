from fastapi import FastAPI
from app.api.routes import quiz
import os
import uvicorn

app = FastAPI(title="Quiz API")

app.include_router(quiz.router, prefix="/api/v1", tags=["quizzes"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Quiz API"}

if __name__ == "__main__":
    ssl_keyfile = os.environ.get("SSL_KEYFILE", "./server.key")
    ssl_certfile = os.environ.get("SSL_CERTFILE", "./server.crt")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)
