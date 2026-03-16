import os

from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Define your agent with OpenAI LLM
hate_speech_detector = Agent(
    role="Hate Speech Detector",
    goal="Analyse the text and identify if any hate speech / offensive language is present",
    llm=llm,
    backstory=(
        "You are a Hate Speech Detector for Social Media who understands details very well and expert negotiator. \
         You can identify hate speech / offensive language in given post."
    ),
)
