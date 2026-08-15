# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse
# # from app.gemini import ask_gemini
# from app.chat import ask_ai, stream_ai

# app = FastAPI()


# @app.get("/")
# def home():
#     return {
#         "message": "AI Chatbot API is running"
#     }


# # @app.get("/chat")
# # def chat(message: str):
# #     # response = ask_gemini(message)
# #     response = ask_ai(message)

# #     return {
# #         "message": message,
# #         "response": response,
# #     }


# @app.get("/chat")
# def chat(
#     session_id: str,
#     message: str,
# ):
#     response = ask_ai(
#         session_id=session_id,
#         message=message,
#     )

#     return {
#         "session_id": session_id,
#         "message": message,
#         "response": response,
#     }


# @app.get("/chat/stream")
# def chat_stream(
#     session_id: str,
#     message: str,
# ):
#     return StreamingResponse(
#         stream_ai(
#             session_id=session_id,
#             message=message,
#         ),
#         media_type="text/plain",
#     )


#### Post Request Example
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.chat import ask_ai, stream_ai
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(
    title="AI Chatbot API",
    description="AI chatbot built with FastAPI, LangChain, Gemini and LangSmith",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "AI Chatbot API is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = ask_ai(
        session_id=request.session_id,
        message=request.message,
    )

    return ChatResponse(
        session_id=request.session_id,
        message=request.message,
        response=response,
    )


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    return StreamingResponse(
        stream_ai(
            session_id=request.session_id,
            message=request.message,
        ),
        media_type="text/plain",
    )