import logging

from src.flows.sales_ops import SalesOpsFlow
from src.flows.marketing_ops import MarketingOpsFlow
from src.flows.customer_success import CustomerSuccessOpsFlow
from src.utils.logging_config import setup_logging, logger
from src.utils.file_validation import validate_csv_files

# Get logger for this module
logger = logging.getLogger(__name__)

# TODO:
# If you are running the docker-compose.yml file, uncomment the following lines.
# However, if your running the individual Dockerfiles, leave these commented out as the ML Flow Server will not be running.

# # Enable MLFlow logging
# import mlflow
# mlflow.crewai.autolog()

# mlflow.set_tracking_uri("http://mlflow:8000")
# mlflow.set_experiment("Autopilot for Executive Reporting")


def kickoff():
    # Setup logging
    setup_logging()

    logger.info("🚀 Kicking off primary flow...")

    # Pre-async run validation of all CSV files
    validate_csv_files()

    # Run all flows
    flows_to_run = [
        [SalesOpsFlow(), "Sales Operations Flow"],
        [MarketingOpsFlow(), "Marketing Operations Flow"],
        [CustomerSuccessOpsFlow(), "Customer Success Operations Flow"],
    ]

    flow_results_list = []
    for flow in flows_to_run:
        logger.info(f"- Starting {flow[1]}")
        flow_result = flow[0].kickoff()
        flow_class = flow[0]
        logger.info(f"- {flow[1]} completed successfully!")
        flow_results_list.append(flow_class)

    # Combine results into a structured output
    sales_ops_flow = flow_results_list[0]
    marketing_ops_flow = flow_results_list[1]
    customer_success_ops_flow = flow_results_list[2]

    combined_result = {
        "sales_ops": {
            "b2c_report": sales_ops_flow.state.b2c_report,
            "b2b_report": sales_ops_flow.state.b2b_report,
        },
        "marketing_ops": {
            "marketing_report": marketing_ops_flow.state.marketing_report,
        },
        "customer_success_ops": {
            "customer_success_report": customer_success_ops_flow.state.customer_success_report,
        },
    }

    return combined_result


def plot():
    sales_ops_flow = SalesOpsFlow()
    sales_ops_flow.plot()


if __name__ == "__main__":
    kickoff()
