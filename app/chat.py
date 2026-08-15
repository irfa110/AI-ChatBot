### Simple AI ChatBot
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


### ChatBot with Prompt Template

# import os

# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
# )

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

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
#             You are an expert Python and Django developer.
#             The user is a software developer learning AI.
#             Explain technical concepts with simple examples.
#             """
#         ),
#         (
#             "human",
#             "{message}"
#         ),
#     ]
# )


# def ask_ai(message: str) -> str:
#     messages = prompt.format_messages(
#         message=message
#     )

#     response = llm.invoke(messages)

#     return response.content

### ChatBot with Memory

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from app.memory import get_history, add_message

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

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
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{message}"
        ),
    ]
)


def ask_ai(session_id: str, message: str) -> str:

    history = get_history(session_id)

    messages = prompt.format_messages(
        history=history,
        message=message,
    )
    print("Messages:", messages)
    response = llm.invoke(messages)

    add_message(
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        session_id,
        AIMessage(content=response.content),
    )

    return response.content


def stream_ai(session_id: str, message: str):

    history = get_history(session_id)

    messages = prompt.format_messages(
        history=history,
        message=message,
    )

    full_response = ""

    for chunk in llm.stream(messages):
        content = chunk.content

        if content:
            full_response += content
            yield content

    add_message(
        session_id,
        HumanMessage(content=message),
    )

    add_message(
        session_id,
        AIMessage(content=full_response),
    )