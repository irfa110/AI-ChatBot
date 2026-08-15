from fastapi import FastAPI
# from app.gemini import ask_gemini
from app.chat import ask_ai

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Chatbot API is running"
    }


# @app.get("/chat")
# def chat(message: str):
#     # response = ask_gemini(message)
#     response = ask_ai(message)

#     return {
#         "message": message,
#         "response": response,
#     }


@app.get("/chat")
def chat(
    session_id: str,
    message: str,
):
    response = ask_ai(
        session_id=session_id,
        message=message,
    )

    return {
        "session_id": session_id,
        "message": message,
        "response": response,
    }