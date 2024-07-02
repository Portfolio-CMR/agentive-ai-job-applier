import textwrap

def gen_body_review(resume_summary: str, job_summary: str, body: str) -> str:
    return textwrap.dedent(f"""
        The 2 provided paragraphs from a cover letter are very poorly written because they \
        do not align the applicant's skills to the needs of the job.

        Rewrite the 2 paragraphs ensuring that the applicant's skills match perfectly \
        with the requirements of the job. 

        Make sure you include quantifiable metrics if they are present in the resume.

        Body: {body}
        Resume details: {resume_summary}
        Job summary: {job_summary}

        expected_output:
        2 paragraph cover letter body that aligns the applicant's skills with the job requirements.
        Do not include explanations, reasoning, or additional commentary.
        Only output the raw text response.
    """)
