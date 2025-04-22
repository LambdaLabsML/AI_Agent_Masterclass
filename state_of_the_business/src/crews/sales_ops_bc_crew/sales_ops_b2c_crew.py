from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.tools.file_read_tool import DatasetFileReadTool
from src.utils.llm_config import LLMConfig

llm = LLMConfig().llm


@CrewBase
class SalesOpsB2CCrew:
    """Crew for generating the B2C sales report."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sales_ops_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_ops_agent"],
            tools=[DatasetFileReadTool()],
            llm=llm,
            verbose=True,
        )

    @task
    def sales_ops_b2c_report(self) -> Task:
        return Task(
            config=self.tasks_config["sales_ops_b2c_report"],
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
            planning=True,
            planning_llm=llm,
        )
