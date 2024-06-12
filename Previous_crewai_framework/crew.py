from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

import openai
import os
import yaml

from dotenv import load_dotenv
load_dotenv()


@CrewBase
class CoverLetterCrew:
    """coverletter crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def job_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['agents']['job_summarizer'],
        )

    @agent
    def resume_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['agents']['resume_summarizer'],
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['agents']['writer'],
        )

    # @task(context={"job_output": job.output, 'resume_output': resume.output})
    # def hook(self, ) -> Task:
    #     return Task(
    #         config=self.tasks_config['tasks']['hook'],
    #         agent=self.writer(),
    #     )

    # @task
    # def body(self, job_output, resume_output, cover_letter_hook_output) -> Task:
    #     return Task(
    #         config=self.tasks_config['tasks']['body'],
    #         agent=self.writer(),
    #         inputs={
    #             'job_output': job_output,
    #             'resume_output': resume_output,
    #             'cover_letter_hook_output': cover_letter_hook_output
    #         }
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the coverletter crew"""


        @task
        def job(self) -> Task:
            return Task(
                config=self.tasks_config['tasks']['job'],
                agent=self.job_summarizer()
            )

        @task
        def resume(self, resume) -> Task:
            return Task(
                config=self.tasks_config['tasks']['resume'],
                agent=self.resume_summarizer(),
                inputs={
                    'input': resume
                }
            )

        job_task = job(self)
        resume_task = resume(self)
        job_result = job_task.execute()
        resume_result = resume_task.execute()

        # Create the hook task AFTER the job and resume tasks are executed
        @task
        def hook(self, job_output, resume_output) -> Task:
            return Task(
                config=self.tasks_config['tasks']['hook'],
                agent=self.writer(),
                inputs={
                    'job_output': job_output,
                    'resume_output': resume_output
                }
            )

        hook_task = hook(self, job_output=job_result, resume_output=resume_result)
        hook_result = hook_task.execute()

        # Create the hook task AFTER the job and resume tasks are executed
        @task
        def body(self, job_output, resume_output, hook_output) -> Task:
            return Task(
                config=self.tasks_config['tasks']['body'],
                agent=self.writer(),
                inputs={
                    'job_output': job_output,
                    'resume_output': resume_output,
                    'hook_output': hook_output
                }
            )

        body_task = body(self, job_output=job_result, resume_output=resume_result, hook_output=hook_result)

        return Crew(
            agents=[self.job_summarizer(), self.resume_summarizer(), self.writer()],
            tasks=[job_task, resume_task, hook_task, body_task],
            process=Process.sequential,
            verbose=True
        )
