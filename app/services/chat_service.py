from collections.abc import Iterator

from langchain_core.messages import AIMessage, HumanMessage

from app.ai.model import llm
from app.ai.prompts import chat_prompt
from app.memory import add_message, get_history


def ask_ai(
    session_id: str,
    message: str,
) -> str:

    history = get_history(session_id)

    messages = chat_prompt.format_messages(
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


def stream_ai(
    session_id: str,
    message: str,
) -> Iterator[str]:

    history = get_history(session_id)

    messages = chat_prompt.format_messages(
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