from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Any, Dict
import uuid
import logging
import asyncio

from models.openai_model import gpt, Message
from models.google import gemini

from prompts.body import gen_body
from prompts.conclusion import gen_conclusion
from prompts.hook import gen_hook
from prompts.job_listing import summarize_job
from prompts.resume import summarize_resume
from prompts.review import gen_body_review
from prompts.truth import gen_truth_check

from utils.jobs import fetch_listing
from utils.read_resume import read_word_document

app = FastAPI()

# --- Persona Definitions ---
talent_acquisition_expert_persona = (
    "You are an expert in talent acquisition and workforce \
        optimization with 20 years of experience summarizing job descriptions."
)

cover_letter_writer_persona = (
    "You are an expert cover letter writer with a comprehensive \
        understanding of Applicant Tracking Systems (ATS) and keyword optimization."
)

resume = read_word_document('secure/resume.docx')

async def generate_letter(url: str, model: str) -> Any:
    job_listing = await fetch_listing(url)
    job_listing_prompt = summarize_job(job_listing)
    resume_prompt = summarize_resume(resume)

    Model = gpt if model == 'gpt' else gemini

    job_summary, resume_summary = await asyncio.gather(
        Model([
            Message(role="system", content=talent_acquisition_expert_persona),
            Message(role="user", content=job_listing_prompt)
        ]),
        Model([
            Message(role="system", content=talent_acquisition_expert_persona),
            Message(role="user", content=resume_prompt)
        ])
    )

    hook = await Model([
        Message(role="system", content=cover_letter_writer_persona),
        Message(role="user", content=gen_hook(resume_summary, job_summary))
    ])

    body = await Model([
        Message(role="system", content=cover_letter_writer_persona),
        Message(role="user", content=gen_body(resume_summary, job_summary, hook))
    ])

    revised_body = await Model([
        Message(role="system", content=cover_letter_writer_persona),
        Message(role="user", content=gen_body_review(resume_summary, job_summary, body))
    ])

    conclusion = await Model([
        Message(role="system", content=cover_letter_writer_persona),
        Message(role="user", content=gen_conclusion(hook, revised_body))
    ])

    final = await Model([
        Message(role="system", content=cover_letter_writer_persona),
        Message(role="user", content=gen_truth_check(resume_summary, hook, revised_body, conclusion))
    ])

