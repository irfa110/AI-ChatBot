from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request

from app.api.routes.chat import router as chat_router
from app.core.exceptions import AIServiceError
from app.core.redis import redis_client
from app.api.routes.auth import router as auth_router

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


@app.get("/health")
def health():

    redis_status = "ok"

    try:

        redis_client.ping()

    except Exception:

        redis_status = "unavailable"

    return {
        "status": "ok",
        "redis": redis_status,
    }


@app.get("/health/live")
def liveness():

    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness():

    redis_client.ping()

    return {
        "status": "ready"
    }

@app.exception_handler(AIServiceError)
async def ai_service_error_handler(
    request: Request,
    exc: AIServiceError,
):

    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc)
        },
    )


app.include_router(chat_router)
app.include_router(auth_router)


# from app.db.database import Base, engine
# Base.metadata.create_all(
#     bind=engine
# )