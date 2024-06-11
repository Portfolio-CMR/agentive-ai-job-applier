from openai import OpenAI
import os

import os
from textwrap import dedent
import docx
from docx import Document


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_name = 'gpt-4o'

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

job_listing = load_document("Materials/job_listing.txt")
resume = load_document("Materials/Robbins_resume.docx")

#####################################################################

# Your entire prompt for the agent
prompt = dedent(f'''

Populate a JSON file based on information from the provided job listing.

job listing: {job_listing}

expected_output:
A JSON-like output with the following information:

Full role:
Company name:
The most important day-to-day challenge for this role:
Skill 1:
Skill 2:
Skill 3:

Do not include explanations, reasoning, or additional commentary.
''')

# API call (using the Chat Completions API)
response = client.chat.completions.create(model=model_name,  # Or another suitable model
messages=[
    {"role": "system", "content": "You are an expert in talent acquisition and workforce optimization with 20 years of experience summarizing job descriptions"},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
job_summary = response.choices[0].message.content
print(job_summary)

###########################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
Your task is to extract information from the resume and output in JSON format.

Extract the name and overall title of the applicant.
Also, extract ALL previous work experiences, including company name, job title,
and the word for word description of job duties found in the resume.

Resume: {resume}

expected_output:
A JSON file with the following format:

Applicant name:
Applicant title:
Applicant email:
Applicant residence:
Applicant portfolio website:
Applicant github:

Previous work experience:
[
{{
    "company": "",
    "title": "",
    "responsibilities": ""
}},
# ... more work experiences as needed
]

Do not include explanations, reasoning, or additional commentary.
''')

# API call (using the Chat Completions API)
response = client.chat.completions.create(model=model_name,  # Or another suitable model
messages=[
    {"role": "system", "content": "You are an expert in talent acquisition and workforce optimization with 20 years of experience summarizing job descriptions."},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
resume_summary = response.choices[0].message.content
print(resume_summary) 

###########################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
Using the provided job summary and resume details, write a compelling opening paragraph (hook) for the cover letter. The hook should:
- Be less than 100 words.
- Highlight the client's experience and qualifications.
- Demonstrate empathy for the most important day-to-day challenge faced in this role. 
- Use keywords that will resonate with ATS scans.
- Incorporate total years experience from the applicant if it appears in the resume.

resume_details: {resume_summary}
job_summary: {job_summary}

expected_output: >
An attention-grabbing cover letter hook (less than 100 words) that addresses why the candidate is well equiped for the most important day-to-day challenge for this role.
The hook should start with:

I was thrilled to see your listing for [role mentioned above], because it is exactly the job I've been looking for."

Do not include explanations, reasoning, or additional commentary.
''')

# API call (using the Chat Completions API)
response = client.chat.completions.create(model=model_name,  # Or another suitable model
messages=[
    {"role": "system", "content": "You are an expert cover letter writer with a comprehensive understanding of Applicant Tracking Systems (ATS) and keyword optimization."},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
hook = response.choices[0].message.content
print(hook) 

###########################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
Based on the provided hook, resume details, and job summary write a cover letter body and conclusion with a strong focus on the company's future needs and how the applicant can fulfill those needs.

- Output the body as two paragraphs.
- Output the conclusion as a single paragraph at the end.
- Ensure the entire length is around 250 words.
- Use relevant and specific accomplishments from the provided resume amd explicitely state why they are critically important for the future of the company.
- All details should heavily focus on why the applicants skills will be beneficial to the future of the company.
- Heavily prioritize unique descriptors and unconventional writing style.

resume_details: {resume_summary}
job_summary: {job_summary}
hook: {hook}

expected_output:
A cover letter body and conclusion with a strong focus on the company's future needs and how the applicant can fulfill those needs.
Do not include explanations, reasoning, or additional commentary.

Do not include explanations, reasoning, or additional commentary.
''')

# API call (using the Chat Completions API)
response = client.chat.completions.create(model=model_name,  # Or another suitable model
messages=[
    {"role": "system", "content": "You are an expert cover letter writer with a comprehensive understanding of Applicant Tracking Systems (ATS) and keyword optimization."},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
body = response.choices[0].message.content
print(body)

def export_to_docx(content, filename="cover_letter.docx"):
    """Exports text content to a Word document (.docx)."""

    document = Document()
    document.add_paragraph(content)
    document.save(filename)

output_file_path = "Finished_cover_letters\cover_letter.docx"
content = f"Dear Hiring Manager,\n\n{hook}\n\n{body}\n\nSincerely\nColton Robbins"
export_to_docx(content, output_file_path)
