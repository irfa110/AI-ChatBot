from langchain_core.messages import HumanMessage
from app.ai.prompts import tool_chat_prompt
from app.memory import add_message, get_history
from langchain_core.messages import AIMessage
from app.ai.content import extract_text
from app.ai.model import llm_with_tools
from app.ai.tool_runner import execute_tool_calls


def ask_with_tools(
    session_id: str,
    message: str,
) -> str:

    history = get_history(session_id)

    messages = tool_chat_prompt.format_messages(
        history=history,
        message=message,
    )

    human_message = HumanMessage(
        content=message
    )

    add_message(
        session_id,
        human_message,
    )

    max_iterations = 5

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:

            add_message(
                session_id,
                response,
            )

            return extract_text(
                response.content
            )

        add_message(
            session_id,
            response,
        )

        tool_messages = execute_tool_calls(
            response
        )

        for tool_message in tool_messages:

            messages.append(tool_message)

            add_message(
                session_id,
                tool_message,
            )

    return "I was unable to complete the request."