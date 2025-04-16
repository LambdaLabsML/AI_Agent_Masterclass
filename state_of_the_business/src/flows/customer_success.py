import logging
from typing import Optional
from crewai.flow.flow import Flow, listen, start

from src.pydantic_models.customer_success import CustomerSuccessOpsState
from src.crews.customer_success_ops.customer_success_ops_crew import (
    CustomerSuccessOpsCrew,
)

# Get logger for this module
logger = logging.getLogger(__name__)


class CustomerSuccessOpsFlow(Flow[CustomerSuccessOpsState]):
    """
    Flow for generating customer success reports and validating data.
    """

    def __init__(self, log_level: Optional[int] = None):
        super().__init__()
        if log_level is not None:
            logger.setLevel(log_level)

    @start()
    def generate_cs_ops_reports(self):
        logger.info("Starting customer success report generation...")

        # Start crew Sales report
        result = (
            CustomerSuccessOpsCrew()
            .crew()
            .kickoff(
                inputs={
                    "cs_sales_data": str(
                        self.state.datasets_dir / "spaceoutfitters_support_data.csv"
                    ),
                }
            )
        )

        # Save the reports to the state
        if result.raw:
            # Store reports with appropriate keys
            self.state.customer_success_report = result.raw
            logger.info("Customer Success reports generated successfully")
        else:
            logger.error("Failed to generate customer success reports")

    @listen(generate_cs_ops_reports)
    def display_cs_ops_report_summaries(self):
        logger.info("Displaying customer success report summaries...")

        # Ensure reports directory exists
        self.state.reports_dir.mkdir(exist_ok=True)

        # Customer Success Report
        logger.info("=== CUSTOMER SUCCESS REPORT SUMMARY ===")
        if self.state.customer_success_report:
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(self.state.customer_success_report.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            logger.info(f"Report summary: {summary}")

            # Save report to file
            report_path = self.state.reports_dir / "customer_success_report.md"
            report_path.write_text(self.state.customer_success_report)
            logger.info(f"Complete report saved to {report_path}")
        else:
            logger.warning("No Customer Success report content available")
