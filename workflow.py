from openai import OpenAI
import os

import os
from textwrap import dedent
import docx
from docx import Document


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_name = 'gpt-3.5-turbo'

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

#####################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
You are an expert in talent acquisition and workforce optimization with 20 years of experience summarizing job descriptions.
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
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
job_summary = response.choices[0].message.content
print(job_summary)

###########################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
You are an expert in talent acquisition and workforce optimization with 20 years of experience summarizing job descriptions.
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
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
resume_summary = response.choices[0].message.content
print(resume_summary) 

###########################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
You are an expert cover letter writer with a comprehensive understanding of Applicant Tracking Systems (ATS) and keyword optimization.

Using the provided job summary and resume details, write a compelling opening paragraph (hook) for the cover letter. The hook should:
- Be less than 100 words.
- Highlight the client's experience and qualifications.
- Demonstrate empathy for the most important day-to-day challenge faced in this role. 
- Use keywords that will resonate with ATS scans.

resume_details: {resume_summary}
job_summary: {job_summary}

expected_output: >
An attention-grabbing cover letter hook (less than 100 words) tailored to the most important day-to-day challenge for this role with relevant keywords throughout.

The hook should start with:

"Dear Hiring Manager,
I was thrilled to see your listing for [role mentioned above], because it is exactly the job I've been looking for."

Do not include explanations, reasoning, or additional commentary.
''')

# API call (using the Chat Completions API)
response = client.chat.completions.create(model=model_name,  # Or another suitable model
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
])
# Get the assistant's response and store it in a variable
hook = response.choices[0].message.content
print(hook) 

###########################################################################

# Your entire prompt for the agent
prompt = dedent(f'''
You are an expert cover letter writer with a comprehensive understanding of Applicant Tracking Systems (ATS) and keyword optimization.
Based on the provided hook, resume details, and job summary write a cover letter body and conclusion with a strong focus on the company's future needs and how the applicant can fulfill those needs.

- Output the body as two paragraphs.
- Output the conclusion as a single paragraph at the end.
- Ensure the entire length is around 250 words.
- Focus on required skills from the job summary.
- Use relevant and specific accomplishments from the provided resume.
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
    {"role": "system", "content": "You are a helpful assistant."},
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

output_file_path = "cover_letter.docx"
content = f"{hook}\n{body}\nSincerely\nColton Robbins"
export_to_docx(content, output_file_path)
