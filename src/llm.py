import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm(temperature=0):
    provider = os.getenv("LLM_PROVIDER", "groq")

    if provider == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperature)

    return ChatGroq(model="openai/gpt-oss-120b", temperature=temperature)