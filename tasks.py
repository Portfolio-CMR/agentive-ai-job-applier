from textwrap import dedent
from crewai import Task
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  


class Tasks():
		def summarize_job(self, agent, job_listing):
				return Task(
						description=(f"""\
								Populate a JSON file based on information from the provided job description.
								
								Job listing: {job_listing}
								"""),
						expected_output=dedent("""\
								A JSON file with the following format:

								Full role:
								Company name:
								The most important day-to-day challenge for this role:
								Skill 1:
								Skill 2:
								Skill 3:
							"""),
						tools=[LLMChain(llm=OpenAI(temperature=0))],
						agent=agent
				)

		def extract_resume_information(self, agent, resume):
				return Task(
						description=dedent(f"""\
							Your task is to extract information from the resume and populate a JSON file.

							Resume: {resume}

							Extract the name and overall title of the applicant.
							Also, extract ALL previous work experiences, including company name, job title, 
							and the word for word description of job duties found in the resume.
						"""),
						expected_output=dedent("""\
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
							"""),
						tools=[LLMChain(llm=OpenAI(temperature=0))],  
						agent=agent
				)

		def create_cover_letter_hook(self, agent, job_summary, resume_details):
				return Task(
						description=dedent(f"""\

								Using the provided job summary and resume details, write a compelling opening paragraph (hook) for the cover letter. The hook should:
								- Be less than 100 words.
								- Highlight the client's experience and qualifications.
								- Demonstrate empathy for the most important day-to-day challenge faced in this role. 
								- Use keywords that will resonate with ATS scans.
								
								Job summary: {job_summary}

								Resume details: {resume_details}

						"""),
						expected_output=dedent("""\
								An attention-grabbing cover letter hook (less than 100 words) tailored to the most important day-to-day challenge for this role with relevant keywords throughout.
								Do not include explanations, reasoning, or additional commentary.
						"""),
						tools=[LLMChain(llm=OpenAI(temperature=1.0))],
						agent=agent
				)

		def create_cover_letter_body(self, agent, job_summary, resume_details, finalized_hook):
				return Task(
						description=dedent(f"""\
								Based on the provided hook, resume details, and job summary write a cover letter body and conclusion with a strong focus on the company's future needs and how the applicant can fulfill those needs.

								- Output the body as two paragraphs.
								- Output the conclusion as a single paragraph at the end.
								- Ensure the entire length is around 250 words.
								- Focus on required skills from the job summary.
								- Use relevant and specific accomplishments from the provided resume.
								- Heavily prioritize unique descriptors and unconventional writing style.

								Job summary: {job_summary}

								Resume details: {resume_details}

								Finalized hook: {finalized_hook}

						"""),
						expected_output=dedent("""\
								A cover letter body and conclusion with a strong focus on the company's future needs and how the applicant can fulfill those needs.
								Do not include explanations, reasoning, or additional commentary.
						"""),
						tools=[LLMChain(llm=OpenAI(temperature=1.0))],
						agent=agent
				)

		def analyze_claims(self, agent, job_summary, resume_details, finalized_hook, finalized_body):
				return Task(
						description=dedent(f"""\
								Given the provided cover letter and resume details, note any inconsistencies between them.

								Your analysis should focus on the following:

								- Verifying Facts: Cross-reference information between the resume and cover letter, checking for alignment in dates, job titles, responsibilities, and accomplishments.
								- Detecting Exaggerations or Embellishments: Scrutinize language for any signs of overstatement or inflation of achievements.
								- Uncovering Potential Fabrications: Look for any claims that seem implausible or too good to be true, and assess their validity.
								- Identifying Omissions: Note any gaps in employment or information that seems to be deliberately left out.
								- Assessing Tone and Style: Compare the tone and writing style of the resume and cover letter to see if they are consistent and professional.

								Finalized hook: {finalized_hook}

								Finalized body: {finalized_body}

								Resume details: {resume_details}

						"""),
						expected_output=dedent("""\
								Provide a detailed report summarizing your findings, highlighting any inconsistencies or concerns you discover. Your report should be objective, factual, and provide specific examples and evidence to support your conclusions.
						"""),
						tools=[LLMChain(llm=OpenAI(temperature=1.0))],
						agent=agent
				)

		def create_cover_letter(self, agent, resume_details, finalized_hook, finalized_body):
				return Task(
						description=dedent(f"""\
								Use the provided resume details to .

								Finalized hook: {finalized_hook}

								Finalized body: {finalized_body}

								Resume details: {resume_details}

						"""),
						expected_output=dedent("""\
								Provide a detailed report summarizing your findings, highlighting any inconsistencies or concerns you discover. Your report should be objective, factual, and provide specific examples and evidence to support your conclusions.
						"""),
						tools=[LLMChain(llm=OpenAI(temperature=1.0))],
						agent=agent
				)