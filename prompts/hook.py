import textwrap

def gen_hook(resume_summary: str, job_summary: str) -> str:
    return textwrap.dedent(f"""
        Using the provided job summary and resume details, write a compelling opening paragraph \
        (hook) for the cover letter. The hook should:
        - Be less than 100 words.
        - Explain why the applicant can successfully take on the challenges of the job outlined \
        in the job summary.
        - Use keywords that will resonate with ATS scans.
        - Incorporate total years experience from the applicant if it appears in the resume.

        Resume details: {resume_summary}
        Job summary: {job_summary}

        expected_output: >
        An attention-grabbing cover letter hook (less than 100 words).
        The hook should start with:

        I was thrilled to see your listing for [role mentioned above], because it is exactly the job \
        I've been looking for."

        Do not include explanations, reasoning, or additional commentary.
        Only output the raw text response.
    """)
