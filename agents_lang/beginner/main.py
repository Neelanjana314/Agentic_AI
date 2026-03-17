from agents import hate_speech_detector
from tasks import HATE_SPEECH_DETECTION_TASK

# Input text to analyze
text = "Public libraries are important resources for everyone in the city."
# text = "That country is less intelligent and incapable of contributing to society."
# text = "People from that race are all untrustworthy and should not be allowed to work in public jobs."

# Run the chain with the task and input text
result = hate_speech_detector.invoke(
    {"task": HATE_SPEECH_DETECTION_TASK.format(text=text)}
)

print("Response:", result.content)
