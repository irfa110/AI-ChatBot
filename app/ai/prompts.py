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