from dotenv import load_dotenv
load_dotenv()
import os

from crewai import Crew
from tasks import Tasks
from agents import Agents

import docx

openai_api_key = os.getenv("OPENAI_API_KEY")

def load_document(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Only TXT and DOCX are supported.")
    return text

tasks = Tasks()
agents = Agents()

job_listing = load_document("job_listing.txt")
resume = load_document("Robbins_resume.docx")

# Create Agents
researcher_agent = agents.research_agent()
resume_agent = agents.resume_agent()
writer_agent = agents.writer_agent()
truth_agent = agents.truth_agent()

# Define Tasks for each agent
job_summary = tasks.summarize_job(researcher_agent, job_listing)
resume_details = tasks.extract_resume_information(resume_agent, resume)
cover_letter_hook = tasks.create_cover_letter_hook(writer_agent, job_summary, resume_details)
cover_letter_body = tasks.create_cover_letter_body(writer_agent, job_summary, resume_details, cover_letter_hook)
# review_and_edit_job_posting_task = tasks.review_and_edit_job_posting_task(review_agent, hiring_needs)

# Instantiate the crew with a sequential process
crew = Crew(
    api_key=openai_api_key,
    agents=[researcher_agent, resume_agent, writer_agent],
    tasks=[
        job_summary,
        resume_details,
        cover_letter_hook,
        cover_letter_body
    ],
    model="gpt-3.5-turbo"
)

# Kick off the process
result = crew.kickoff()

print("Cover Letter Creation Process Completed.")
print("Final Cover Letter:")
print(result)