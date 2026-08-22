from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import (ask_ai, stream_ai,
                                       ask_ai_async, stream_ai_async)

from app.services.stream_tool_chat_service import stream_with_tools
from app.services.tool_chat_service import ask_with_tools
from fastapi import Depends
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, user_id: str = Depends(get_current_user)):

    response = ask_ai(
        user_id=user_id,
        session_id=request.session_id,
        message=request.message,
    )

    return ChatResponse(
        session_id=request.session_id,
        message=request.message,
        response=response,
    )

@router.post("/stream")
def chat_stream(request: ChatRequest, user_id: str = Depends(get_current_user)):

    return StreamingResponse(
        stream_ai(
            user_id=user_id,
            session_id=request.session_id,
            message=request.message,
        ),
        media_type="text/plain",
    )


@router.post("/async", response_model=ChatResponse)
async def chat_async(request: ChatRequest, user_id: str = Depends(get_current_user)):

    response = await ask_ai_async(
        user_id=user_id,
        session_id=request.session_id,
        message=request.message,
    )

    return ChatResponse(
        session_id=request.session_id,
        message=request.message,
        response=response,
    )


@router.post("/async/stream")
async def chat_async_stream(request: ChatRequest, user_id: str = Depends(get_current_user)):

    return StreamingResponse(
        stream_ai_async(
            user_id=user_id,
            session_id=request.session_id,
            message=request.message,
        ),
        media_type="text/plain",
    )

@router.post("/tools")
def chat_with_tools(request: ChatRequest, user_id: str = Depends(get_current_user)):

    response = ask_with_tools(
        user_id=user_id,
        session_id=request.session_id,
        message=request.message,
    )

    return {
        "message": request.message,
        "response": response,
    }


@router.post("/tools/stream")
def stream_chat(request: ChatRequest, user_id: str = Depends(get_current_user)):

    return StreamingResponse(
        stream_with_tools(
            user_id=user_id,
            session_id=request.session_id,
            message=request.message,
        ),
        media_type="text/plain",
    )