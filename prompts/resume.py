import textwrap

def summarize_resume(resume: str) -> str:
    return textwrap.dedent(f"""
        Your task is to extract information from the resume and output in JSON format.

        - Extract contact information for the applicant
        - Also, extract ALL previous work experiences, including company name, job title,
        and the description of job duties found in the resume.
        - Ensure that the description of job duties is extracted exactly as it is written in the
        resume.
        - Write the applicant's name in title case.
        - Reformat all company names in title case.

        Resume: {resume}

        expected_output:
        A JSON file with the following format:

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
        Only output the raw text response.
        Make sure the company names are Capitalized correctly.
    """)
