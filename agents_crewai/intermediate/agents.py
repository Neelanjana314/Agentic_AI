import os

from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

from tools import exa_search_tool, log_reader_tool

llm = LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def system_template_devops():
    """Custom system template for DevOps agents"""
    return """You are an expert DevOps engineer with extensive experience in:
    - Infrastructure automation and orchestration
    - Container technologies (Docker, Kubernetes)
    - CI/CD pipelines and deployment strategies
    - Monitoring, logging, and observability
    - Cloud platforms (AWS, GCP, Azure)
    - Security best practices and compliance
    
    Always provide:
    1. Detailed technical analysis
    2. Step-by-step solutions
    3. Best practices and recommendations
    4. Risk assessment and mitigation strategies
    5. References to official documentation
    
    Focus on practical, production-ready solutions."""


# Agent 1: Log Analyzer - Analyzes log files to identify issues
log_analyzer = Agent(
    role="DevOps Log Analyzer",
    goal="Analyze log files to identify and extract specific issues, errors, and failure patterns",
    llm=llm,
    backstory="""You are a senior DevOps engineer with 10 years of experience in 
    analyzing production logs and identifying critical issues. You excel at parsing 
    through complex log files, identifying error patterns, extracting relevant error 
    messages, and determining the root cause of failures from log data.""",
    tools=[log_reader_tool],
    verbose=True,
    respect_context_window=True,  # Respect model's context window
    max_iter=3,
    max_execution_time=300,  # 5 minutes max execution time
    max_rpm=10,  # Rate limiting: max 10 requests per minute
    system_template=system_template_devops(),
)

# Agent 2: Issue Investigator - Searches for solutions online
issue_investigator = Agent(
    role="DevOps Issue Investigator",
    goal="Investigate identified issues by searching documentation, forums, and known solutions online",
    llm=llm,
    backstory="""You are a DevOps troubleshooting specialist who excels at quickly 
    finding solutions to technical problems. You know how to search effectively for 
    similar issues, identify reliable sources, and gather comprehensive information 
    about error patterns and their solutions.""",
    tools=[exa_search_tool],
    verbose=True,
    respect_context_window=True,
    max_iter=5,
    max_execution_time=600,  # 10 minutes for thorough investigation
    max_rpm=15,  # Higher rate limit for search operations
    system_template=system_template_devops(),
)

# Agent 3: Solution Specialist - Provides actionable solutions
solution_specialist = Agent(
    role="DevOps Solution Specialist",
    goal="Provide clear, actionable solutions with step-by-step instructions based on investigation findings",
    llm=llm,
    backstory="""You are a DevOps solutions architect who specializes in creating 
    reliable, step-by-step remediation plans for infrastructure and deployment issues. 
    You always provide official documentation references, tested solutions, and 
    preventive measures to avoid future occurrences.""",
    verbose=True,
    respect_context_window=True,
    max_iter=4,
    max_execution_time=450,  # 7.5 minutes for comprehensive solutions
    max_rpm=8,  # Conservative rate limit for solution generation
    system_template=system_template_devops(),
)

# Agent 4: Code Fix Generator - Generates actual code/config fixes
code_fix_generator = Agent(
    role="DevOps Code Fix Generator",
    goal="Generate production-ready code patches, configuration fixes, and automation scripts based on the solution plan",
    llm=llm,
    backstory="""You are a senior DevOps developer who specializes in writing clean,
    production-ready infrastructure code. You excel at writing Kubernetes manifests,
    Dockerfiles, CI/CD pipeline configs, shell scripts, and infrastructure-as-code
    templates. You always include inline comments, error handling, and follow best
    practices for maintainability and security.""",
    verbose=True,
    respect_context_window=True,
    max_iter=4,
    max_execution_time=450,  # 7.5 minutes for code generation
    max_rpm=10,
    system_template=system_template_devops(),
)
