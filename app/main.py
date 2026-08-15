from fastapi import FastAPI
from app.gemini import ask_gemini

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Chatbot API is running"
    }


@app.get("/chat")
def chat(message: str):
    response = ask_gemini(message)

    return {
        "message": message,
        "response": response,
    }