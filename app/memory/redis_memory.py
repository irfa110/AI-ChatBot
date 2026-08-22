import json

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    BaseMessage,
)

from app.core.redis import redis_client


def get_history(user_id: str, session_id: str) -> list[BaseMessage]:

    # key = f"chat:{session_id}"
    key = f"chat:{user_id}:{session_id}"
    raw_messages = redis_client.lrange(
        key,
        0,
        -1,
    )

    return [
        deserialize_message(
            json.loads(raw_message)
        )
        for raw_message in raw_messages
    ]


def add_message(
    user_id: str,
    session_id: str,
    message: BaseMessage,
) -> None:

    key = f"chat:{user_id}:{session_id}"

    if isinstance(message, HumanMessage):
        message_type = "human"

    elif isinstance(message, AIMessage):
        message_type = "ai"

    else:
        return

    # data = {
    #     "type": message_type,
    #     "content": message.content,
    # }
    data = serialize_message(message)

    redis_client.rpush(
        key,
        json.dumps(data),
    )

    redis_client.expire(
    key,
    60 * 60 * 24,
    )


def serialize_message(message: BaseMessage) -> dict:

    if isinstance(message, HumanMessage):

        return {
            "type": "human",
            "content": message.content,
        }

    if isinstance(message, AIMessage):

        return {
            "type": "ai",
            "content": message.content,
            "tool_calls": message.tool_calls,
        }

    if isinstance(message, ToolMessage):

        return {
            "type": "tool",
            "content": message.content,
            "tool_call_id": message.tool_call_id,
        }

    raise ValueError(
        f"Unsupported message type: {type(message)}"
    )


def deserialize_message(data: dict) -> BaseMessage:

    message_type = data["type"]

    if message_type == "human":

        return HumanMessage(
            content=data["content"]
        )

    if message_type == "ai":

        return AIMessage(
            content=data["content"],
            tool_calls=data.get("tool_calls", []),
        )

    if message_type == "tool":

        return ToolMessage(
            content=data["content"],
            tool_call_id=data["tool_call_id"],
        )

    raise ValueError(
        f"Unsupported message type: {message_type}"
    )