import os

from crewai import Crew, Process
from tasks import (analyze_logs_task, investigate_issue_task,
                   provide_solution_task, generate_code_fix_task)

from agents import issue_investigator, log_analyzer, solution_specialist, code_fix_generator

# Enhanced DevOps crew with advanced configuration
devops_crew = Crew(
    agents=[log_analyzer, issue_investigator, solution_specialist, code_fix_generator],
    tasks=[analyze_logs_task, investigate_issue_task, provide_solution_task, generate_code_fix_task],
    verbose=True,
    process=Process.sequential,
    cache=True,
    max_rpm=30,
)

if __name__ == "__main__":
    print("🚀 Starting Enhanced DevOps Issue Analysis...")

    # Scenario 1: Analyze Kubernetes deployment error
    print("\n📋 Scenario 1: Kubernetes Deployment Analysis")
    result = devops_crew.kickoff(
        inputs={"log_file_path": "../dummy_logs/kubernetes_deployment_error.log"}
    )

    # Scenario 2: Analyze database connection error
    # print("\n📋 Scenario 2: Database Connection Analysis")
    # result = devops_crew.kickoff(inputs={"log_file_path": "../dummy_logs/database_connection_error.log"})

    print("\n🎉 DevOps analysis completed!")
