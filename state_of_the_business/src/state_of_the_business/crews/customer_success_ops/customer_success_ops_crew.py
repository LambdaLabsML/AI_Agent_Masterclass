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
class CustomerSuccessOpsCrew:
    """Customer Success Ops Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def customer_success_ops_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_success_ops_agent"],
            tools=[DatasetFileReadTool()],
            llm=llm,
        )

    @task
    def cs_ops_performance_report(self) -> Task:
        return Task(
            config=self.tasks_config["cs_ops_board_report"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Customer Success Ops Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            full_output=True,
        )
