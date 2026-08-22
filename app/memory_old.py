from collections import defaultdict

from langchain_core.messages import BaseMessage


chat_history: dict[str, list[BaseMessage]] = defaultdict(list)


def get_history(session_id: str) -> list[BaseMessage]:
    return chat_history[session_id]


def add_message(
    session_id: str,
    message: BaseMessage,
) -> None:
    chat_history[session_id].append(message)