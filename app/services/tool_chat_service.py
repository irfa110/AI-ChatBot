from langchain_core.messages import HumanMessage
from app.ai.prompts import tool_chat_prompt
from app.ai.content import extract_text
from app.ai.model import llm_with_tools
from app.ai.tool_runner import execute_tool_calls


# def ask_with_tools(message: str) -> str:

#     messages = [
#         HumanMessage(content=message)
#     ]

#     response = llm_with_tools.invoke(messages)

#     if not response.tool_calls:
#         return response.content

#     tool_messages = execute_tool_calls(response)

#     messages.append(response)
#     messages.extend(tool_messages)

#     final_response = llm_with_tools.invoke(messages)

#     return final_response.content

# def ask_with_tools(message: str) -> str:

#     messages = [
#         HumanMessage(content=message)
#     ]

#     max_iterations = 5

#     for _ in range(max_iterations):

#         response = llm_with_tools.invoke(messages)

#         print("CONTENT:", response.content)
#         print("TYPE:", type(response.content))
#         print("TOOL CALLS:", response.tool_calls)

#         if not response.tool_calls:
#             return response.content

#         messages.append(response)

#         tool_messages = execute_tool_calls(response)

#         messages.extend(tool_messages)

#     return "I was unable to complete the request."

def ask_with_tools(message: str) -> str:

    messages = tool_chat_prompt.format_messages(
        message=message
    )

    max_iterations = 5

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        if not response.tool_calls:
            return extract_text(response.content)

        messages.append(response)

        tool_messages = execute_tool_calls(response)

        messages.extend(tool_messages)

    return "I was unable to complete the request."