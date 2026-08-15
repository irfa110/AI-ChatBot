from langchain_core.messages import ToolMessage

from app.tools.calculator import calculator
from app.tools.time import get_current_utc_time


tools = {
    calculator.name: calculator,
    get_current_utc_time.name: get_current_utc_time,
}


def execute_tool_calls(response):

    tool_messages = []

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        tool = tools.get(tool_name)

        if not tool:
            continue

        result = tool.invoke(tool_args)

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call_id,
            )
        )

    return tool_messages