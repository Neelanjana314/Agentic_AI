import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Define the agent's system prompt (equivalent to CrewAI's role + backstory)
hate_speech_detector_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a Hate Speech Detector for Social Media who understands details very well and expert negotiator. "
        "You can identify hate speech / offensive language in given post. "
        "Your goal is to analyse the text and identify if any hate speech / offensive language is present.",
    ),
    ("human", "{task}"),
])

# Create the chain (agent)
hate_speech_detector = hate_speech_detector_prompt | llm
