import textwrap

def gen_truth_check(resume_summary: str, hook: str, body: str, conclusion: str) -> str:
    return textwrap.dedent(f"""
        Analyze the provided cover letter hook and body and compare them against the provided resume. 
        Identify any statements in the cover letter that are inconsistent with, or not supported by, \
        the details in the resume. 
        Rewrite the false statements so that they are accurately represented.
        Do not change the first sentence of the hook.

        Hook: {hook}
        Body: {body}
        Conclusion: {conclusion}
        Resume details: {resume_summary}

        expected_output:
        A single revised cover letter with line breaks between paragraphs.
        Only output the raw text response.
        Do not include explanations, reasoning, or additional commentary.
    """)
