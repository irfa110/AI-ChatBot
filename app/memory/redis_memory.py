import json

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    BaseMessage,
)

from app.core.redis import redis_client


def get_history(session_id: str) -> list[BaseMessage]:

    key = f"chat:{session_id}"

    raw_messages = redis_client.lrange(
        key,
        0,
        -1,
    )

    messages = []

    for raw_message in raw_messages:

        data = json.loads(raw_message)

        if data["type"] == "human":

            messages.append(
                HumanMessage(
                    content=data["content"]
                )
            )

        elif data["type"] == "ai":

            messages.append(
                AIMessage(
                    content=data["content"]
                )
            )

    return messages


def add_message(
    session_id: str,
    message: BaseMessage,
) -> None:

    key = f"chat:{session_id}"

    if isinstance(message, HumanMessage):
        message_type = "human"

    elif isinstance(message, AIMessage):
        message_type = "ai"

    else:
        return

    data = {
        "type": message_type,
        "content": message.content,
    }

    redis_client.rpush(
        key,
        json.dumps(data),
    )

    redis_client.expire(
    key,
    60 * 60 * 24,
    )