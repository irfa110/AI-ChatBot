from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import (ask_ai, stream_ai,
                                       ask_ai_async, stream_ai_async)

from app.services.tool_chat_service import ask_with_tools

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


@router.post("/async", response_model=ChatResponse)
async def chat_async(request: ChatRequest):

    response = await ask_ai_async(
        session_id=request.session_id,
        message=request.message,
    )

    return ChatResponse(
        session_id=request.session_id,
        message=request.message,
        response=response,
    )


@router.post("/async/stream")
async def chat_async_stream(request: ChatRequest):

    return StreamingResponse(
        stream_ai_async(
            session_id=request.session_id,
            message=request.message,
        ),
        media_type="text/plain",
    )

@router.post("/tools")
def chat_with_tools(request: ChatRequest):

    response = ask_with_tools(
        session_id=request.session_id,
        message=request.message,
    )

    return {
        "message": request.message,
        "response": response,
    }
