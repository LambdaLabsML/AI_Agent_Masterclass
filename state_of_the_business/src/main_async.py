import logging
import asyncio

from src.flows.sales_ops import SalesOpsFlow
from src.flows.marketing_ops import MarketingOpsFlow
from src.flows.customer_success import CustomerSuccessOpsFlow
from src.utils.logging_config import setup_logging, logger
from src.utils.file_validation import validate_csv_files

# Get logger for this module
logger = logging.getLogger(__name__)

# TODO: 
    # If you are running the docker-compose.yml file, uncomment the following lines (part 2).
    # However, if your running the individual Dockerfiles, leave these commented out as the ML Flow Server will not be running.

# # Enable MLFlow logging
# import mlflow
# mlflow.crewai.autolog()

# mlflow.set_tracking_uri("http://mlflow:8000")
# mlflow.set_experiment("Autopilot for Executive Reporting")


async def run_flow(flow_class, flow_name):
    logger.info(f"- Starting {flow_name}")
    flow = flow_class()
    # # TODO: add line to kick off the flow async
    # result = await flow.kickoff_async()
    logger.info(f"- {flow_name} completed successfully!")
    return flow, result


async def kickoff():
    # Setup logging
    setup_logging()

    logger.info("🚀 Kicking off primary flow...")

    # Pre-async run validation of all CSV files
    validate_csv_files()

    # TODO: Create the tasks for each flow
    tasks = []

    # Run all flows concurrently and wait for completion
    # TODO: 
    results = await asyncio.gather(*tasks)
    print(f"Final Results: {results}")

    # Unpack results
    sales_ops_flow, _ = results[0]
    marketing_ops_flow, _ = results[1]
    customer_success_ops_flow, _ = results[2]

    # Combine results into a structured output
    combined_result = {
        "sales_ops": {
            "b2c_report": sales_ops_flow.state.b2c_report,
            "b2b_report": sales_ops_flow.state.b2b_report,
        },
        "marketing_ops": {
            "marketing_report": marketing_ops_flow.state.marketing_report
        },
        "customer_success_ops": {
            "customer_success_report": customer_success_ops_flow.state.customer_success_report
        },
    }

    print(f"Combined Results: {combined_result}")
    return combined_result


def plot():
    sales_ops_flow = SalesOpsFlow()
    sales_ops_flow.plot()


if __name__ == "__main__":
    asyncio.run(kickoff())
