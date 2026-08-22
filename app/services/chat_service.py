from collections.abc import Iterator

from langchain_core.messages import AIMessage, HumanMessage
from app.ai.model import llm
from app.ai.prompts import chat_prompt
from app.memory import add_message, get_history
from app.ai.model import llm_with_tools
from app.core.exceptions import AIServiceError


def ask_ai(
    user_id: str,
    session_id: str,
    message: str,
) -> str:

    history = get_history(user_id, session_id)

    messages = chat_prompt.format_messages(
        history=history,
        message=message,
    )
    try:
        response = llm.invoke(messages)
    except Exception as exc:
        raise AIServiceError(
            "AI service temporarily unavailable"
        ) from exc

    add_message(
        user_id,
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        user_id,
        session_id,
        AIMessage(content=response.content),
    )

    return response.content


def stream_ai(
    user_id: str,
    session_id: str,
    message: str,
) -> Iterator[str]:

    history = get_history(user_id, session_id)

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
        user_id,
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        user_id,
        session_id,
        AIMessage(content=full_response),
    )


async def ask_ai_async(
    user_id: str,
    session_id: str,
    message: str,
) -> str:

    history = get_history(user_id, session_id)

    messages = chat_prompt.format_messages(
        history=history,
        message=message,
    )

    response = await llm.ainvoke(messages)

    add_message(
        user_id,
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        user_id,
        session_id,
        AIMessage(content=response.content),
    )

    return response.content


async def stream_ai_async(
    user_id: str,
    session_id: str,
    message: str,
):

    history = get_history(user_id, session_id)

    messages = chat_prompt.format_messages(
        history=history,
        message=message,
    )

    full_response = ""

    async for chunk in llm.astream(messages):

        content = chunk.content

        if content:

            full_response += content

            yield content

    add_message(
        user_id,
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        user_id,
        session_id,
        AIMessage(content=full_response),
    )


def test_tool_call(message: str):

    response = llm_with_tools.invoke(message)

    print("Response:", response)
    print("Tool calls:", response.tool_calls)

    return response