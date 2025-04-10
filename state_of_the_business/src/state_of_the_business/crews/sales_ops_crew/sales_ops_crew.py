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
class SalesOpsCrew:
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
    
    @task
    def sales_ops_b2c_report(self) -> Task:
        return Task(
            config=self.tasks_config["sales_ops_b2c_report"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            full_output=True,
        )
        
        # Store original kickoff method
        original_kickoff = crew_instance.kickoff
        
        # Override kickoff to provide custom output structure
        def kickoff_with_structured_output(*args, **kwargs):
            # Call original kickoff
            result = original_kickoff(*args, **kwargs)
            
            # Store outputs from each task in a dictionary
            reports = {}
            
            # Get output for each task if available
            for i, task in enumerate(crew_instance.tasks):
                task_id = task.id
                # Access task outputs from crew_instance.outputs
                if task_id in crew_instance.outputs:
                    task_name = 'sales_ops_b2c_report' if i == 0 else 'sales_ops_b2b_report'
                    reports[task_name] = crew_instance.outputs[task_id]
            
            # Make reports available in result
            result.raw = reports
            return result
        
        # Replace original kickoff with our custom version
        crew_instance.kickoff = kickoff_with_structured_output
        return crew_instance
