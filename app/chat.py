from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.memory import get_history, add_message
settings = get_settings()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.gemini_api_key,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert Python and Django developer.
            The user is a software developer learning AI.
            Explain technical concepts with simple examples.
            """
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{message}"
        ),
    ]
)


def ask_ai(session_id: str, message: str) -> str:

    history = get_history(session_id)

    messages = prompt.format_messages(
        history=history,
        message=message,
    )
    response = llm.invoke(messages)

    add_message(
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        session_id,
        AIMessage(content=response.content),
    )

    return response.content


def stream_ai(session_id: str, message: str):

    history = get_history(session_id)

    messages = prompt.format_messages(
        history=history,
        message=message,
    )

    full_response = ""

    for chunk in llm.stream(messages):
        content = chunk.content

        if content:
            full_response += content
            yield content

    add_message(
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        session_id,
        AIMessage(content=full_response),
    )