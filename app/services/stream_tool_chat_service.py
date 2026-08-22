from langchain_core.messages import HumanMessage, AIMessage

from app.ai.content import extract_text
from app.ai.model import llm_with_tools
from app.ai.prompts import tool_chat_prompt
from app.ai.tool_runner import execute_tool_calls
from app.memory import get_history, add_message

def stream_with_tools(
    user_id: str,
    session_id: str,
    message: str,
):

    history = get_history(user_id, session_id)

    messages = tool_chat_prompt.format_messages(
        history=history,
        message=message,
    )

    human_message = HumanMessage(
        content=message
    )

    add_message(
        user_id,
        session_id,
        human_message,
    )

    max_iterations = 5

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        # No tool required
        if not response.tool_calls:

            answer = extract_text(
                response.content
            )

            add_message(
                user_id,
                session_id,
                AIMessage(
                    content=answer
                ),
            )

            # Stream the already generated answer
            yield answer

            return

        # Save AI tool call
        add_message(
            user_id,
            session_id,
            response,
        )

        # Execute tools
        tool_messages = execute_tool_calls(
            response
        )

        for tool_message in tool_messages:

            messages.append(tool_message)

            add_message(
                user_id,
                session_id,
                tool_message,
            )

        # Continue loop
        # Gemini will now generate the final response