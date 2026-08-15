# import os

# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
# )


# def ask_ai(message: str) -> str:
#     response = llm.invoke(message)

#     return response.content

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful AI assistant. "
#             "Answer clearly and concisely."
#         ),
#         (
#             "human",
#             "{message}"
#         ),
#     ]
# )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert Python and Django developer.
            The user is a software developer learning AI.
            Explain technical concepts with simple examples.
            """
        ),
        (
            "human",
            "{message}"
        ),
    ]
)


def ask_ai(message: str) -> str:
    messages = prompt.format_messages(
        message=message
    )

    response = llm.invoke(messages)

    return response.content