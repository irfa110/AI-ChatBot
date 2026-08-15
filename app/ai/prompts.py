from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)


chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert Python and Django developer.

            The user is a software developer learning AI.

            Explain technical concepts with simple examples.
            """
        ),
        MessagesPlaceholder(
            variable_name="history"
        ),
        (
            "human",
            "{message}"
        ),
    ]
)


tool_chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert Python and Django developer.

            The user is a software developer learning AI.

            Explain technical concepts with simple examples.

            You have access to tools.
            Use a tool when it is useful.
            Do not use a tool when you can answer directly.
            """
        ),
        (
            "human",
            "{message}"
        ),
    ]
)