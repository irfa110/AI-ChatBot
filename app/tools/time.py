from datetime import datetime, timezone

from langchain_core.tools import tool


@tool
def get_current_utc_time() -> str:
    """
    Get the current UTC time.

    Use this tool when the user asks for the current time.
    """

    return datetime.now(timezone.utc).isoformat()