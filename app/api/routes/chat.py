from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ask_ai, stream_ai


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
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


@router.post("/stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        stream_ai(
            session_id=request.session_id,
            message=request.message,
        ),
        media_type="text/plain",
    )