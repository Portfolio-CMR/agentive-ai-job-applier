import textwrap

def summarize_job(job_listing: str) -> str:
    return textwrap.dedent(f"""
        Populate a JSON file based on information from the provided job listing.

        Job listing: {job_listing}

        expected_output:
        A JSON-like output with the following information:

        Full role:
        Company name:
        The most important day-to-day challenge for this role:
        Skill 1:
        Skill 2:
        Skill 3:
        Skill 4:
        Skill 5:

        Do not include explanations, reasoning, or additional commentary.
    """)
