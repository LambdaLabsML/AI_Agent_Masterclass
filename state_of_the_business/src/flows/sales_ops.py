import logging
from typing import Optional
from crewai.flow.flow import Flow, listen, start

from src.pydantic_models.sales_ops import SalesOpsState
from src.crews.sales_ops_bc_crew.sales_ops_b2c_crew import SalesOpsB2CCrew
from src.crews.sales_ops_bb_crew.sales_ops_b2b_crew import SalesOpsB2BCrew


# Get logger for this module
logger = logging.getLogger(__name__)


# Sales Operations Flow
class SalesOpsFlow(Flow[SalesOpsState]):
    """
    Flow for generating sales reports for both B2C and B2B.
    """

    def __init__(self, log_level: Optional[int] = None):
        super().__init__()
        if log_level is not None:
            logger.setLevel(log_level)

    @start()
    def generate_b2c_sales_reports(self):
        logger.info("Starting B2C sales report generation...")

        # Start crew Sales report
        result = _________.crew().kickoff(
            inputs={
                "month": "03",
                "year": "2025",
                "b2c_sales_data": str(
                    self.state.datasets_dir / "spaceoutfitters_b2c_sales.csv"
                ),
            }
        )

        # Save the reports to the state
        if result.raw:
            # Store reports with appropriate keys
            self.state.b2c_report = result.raw
            logger.info("B2C sales reports generated successfully")
        else:
            logger.error("Failed to generate B2C sales reports")

    @listen(generate_b2c_sales_reports)
    def display_report_summaries(self):
        logger.info("Displaying report summaries...")

        # Ensure reports directory exists
        self.state.reports_dir.mkdir(exist_ok=True)

        # B2C Report
        logger.info("=== B2C REPORT SUMMARY ===")
        if self.state.b2c_report:
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(self.state.b2c_report.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            logger.info(f"Report summary: {summary}")

            # Save report to file
            report_path = self.state.reports_dir / "b2c_report.md"
            report_path.write_text(self.state.b2c_report)
            logger.info(f"Complete report saved to {report_path}")
        else:
            logger.warning("No B2C report content available")

    @listen(generate_b2c_sales_reports)
    def generate_b2b_sales_reports(self):
        logger.info("Starting B2B sales report generation...")

        # Start crew Sales report
        result = _________.crew().kickoff(
            inputs={
                "month": "03",
                "year": "2025",
                "b2b_sales_data": str(
                    self.state.datasets_dir / "spaceoutfitters_b2b_sales_lite.csv"
                ),
            }
        )

        # Save the reports to the state
        if result.raw:
            # Store reports with appropriate keys
            self.state.b2b_report = result.raw
            logger.info("B2B sales reports generated successfully")
        else:
            logger.error("Failed to generate B2B sales reports")

    @listen(generate_b2b_sales_reports)
    def display_b2b_report_summaries(self):
        logger.info("Displaying B2B report summaries...")

        # Ensure reports directory exists
        self.state.reports_dir.mkdir(exist_ok=True)

        # B2B Report
        logger.info("=== B2B REPORT SUMMARY ===")
        if self.state.b2b_report:
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(self.state.b2b_report.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            logger.info(f"Report summary: {summary}")

            # Save report to file
            report_path = self.state.reports_dir / "b2b_report.md"
            report_path.write_text(self.state.b2b_report)
            logger.info(f"Complete report saved to {report_path}")
        else:
            logger.warning("No B2B report content available")


# SalesOpsB2CCrew()
# SalesOpsB2BCrew()
