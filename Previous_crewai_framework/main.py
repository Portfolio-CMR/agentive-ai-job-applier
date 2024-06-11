import os
from dotenv import load_dotenv
load_dotenv()

import docx

from Previous_crewai_framework.crew import CoverLetterCrew

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

job_listing = load_document("job_listing.txt")
resume = load_document("Robbins_resume.docx")

def run():
    inputs = {
        'job_listing': job_listing,
        'resume': resume
    }
    CoverLetterCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()