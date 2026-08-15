from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.tools.calculator import calculator
from app.tools.time import get_current_utc_time

settings = get_settings()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.gemini_api_key,
)

llm_with_tools = llm.bind_tools(
    [calculator, get_current_utc_time,]
)