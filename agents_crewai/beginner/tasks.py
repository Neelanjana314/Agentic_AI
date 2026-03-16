from crewai import Task

from agents import hate_speech_detector

# Define a task with a description and expected output
hate_speech_detection_task = Task(
    description=(
        "Analyze the following text to determine if it contains any hate speech or offensive language. "
        "Follow these steps:\n"
        "1. Read the text carefully.\n"
        "2. Identify any language that targets a group or individual based on attributes such as race, ethnicity, gender, religion, nationality, disability, or sexual orientation.\n"
        "3. Look for threats, dehumanizing language, insults, or promotion of violence or hatred.\n"
        "4. Evaluate the context to ensure words or phrases are not taken out of context.\n"
        "5. Make an objective decision based on the content.\n"
        "Text:\n{text}"
    ),
    expected_output="Respond with 'hate speech' / 'no hate speech' and a brief explanation of your reasoning.",
    agent=hate_speech_detector,
)
