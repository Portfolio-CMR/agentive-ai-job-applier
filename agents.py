from crewai import Agent
from crewai_tools.tools import WebsiteSearchTool, FileReadTool, DOCXSearchTool, JSONSearchTool


class Agents():
	def research_agent(self):
		return Agent(
			role='Research Analyst',
			goal='Analyze and summarize the job listing for the most important information',
			backstory='You are an expert in talent acquisition and workforce optimization with 20 years of experience summarizing job descriptions.',
			verbose=True
		)

	def resume_agent(self):
		return Agent(
			role='Career Summarizer',
			goal='Analyze and summarize the resume for job experience and applicant information',
			backstory='You are an expert in talent acquisition and workforce optimization with 20 years of experience summarizing job descriptions.',
			verbose=True
		)

	def writer_agent(self):
			return Agent(
				role='Career Writer',
				goal='Use insights from job listing summary and applicant resume to create a detailed, engaging, and enticing cover letter.',
				backstory='You are an expert cover letter writer with a comprehensive understanding of Applicant Tracking Systems (ATS) and keyword optimization.',
				verbose=True
			)

	def truth_agent(self):
			return Agent(
				role='Analyze Claims',
				goal='Review application materials against an applicant\'s resume and identify any inconsistencies',
				backstory='You are an expert Truth Seeker who is adept at identifying false claims and inconsistencies.',
				verbose=True
			)
