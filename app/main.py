from fastapi import FastAPI

from app.api.routes.chat import router as chat_router


app = FastAPI(
    title="AI Chatbot API",
    description=(
        "AI chatbot built with "
        "FastAPI, LangChain, Gemini and LangSmith"
    ),
    version="0.1.0",
)


@app.get("/")
def home():

    return {
        "message": "AI Chatbot API is running"
    }


app.include_router(chat_router)