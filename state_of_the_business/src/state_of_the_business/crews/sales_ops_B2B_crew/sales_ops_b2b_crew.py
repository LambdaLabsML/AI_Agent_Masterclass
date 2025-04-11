import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
from state_of_the_business.tools.file_read_tool import DatasetFileReadTool

llm = LLM(
    base_url=os.getenv("LAMBDA_API_BASE"),
    model="openai/llama-4-maverick",
    api_key=os.getenv("LAMBDA_API_KEY"),
)


@CrewBase
class SalesOpsB2BCrew:
    """Sales Ops Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sales_ops_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_ops_agent"],
            tools=[DatasetFileReadTool()],
            llm=llm,
        )

    @task
    def sales_ops_b2b_report(self) -> Task:
        return Task(
            config=self.tasks_config["sales_ops_b2b_report"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Sales Ops Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            full_output=True,
        )
