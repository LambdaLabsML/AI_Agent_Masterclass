import logging
from typing import Optional
from crewai.flow.flow import Flow, listen, start

from src.pydantic_models.marketing_opps import MarketingOpsState
from src.crews.mkt_ops_crew.mkt_ops_crew import MktOpsCrew

# Get logger for this module
logger = logging.getLogger(__name__)


class MarketingOpsFlow(Flow[MarketingOpsState]):
    """
    Flow for generating marketing operations reports.
    """

    def __init__(self, log_level: Optional[int] = None):
        super().__init__()
        if log_level is not None:
            logger.setLevel(log_level)

    @start()
    def generate_mkt_ops_reports(self):
        logger.info("Starting marketing report generation...")

        try:
            # Start crew Sales report
            result = (
                MktOpsCrew()
                .crew()
                .kickoff(
                    inputs={
                        "month": "03",
                        "year": "2025",
                        "mkt_ops_data": str(
                            self.state.datasets_dir
                            / "spaceoutfitters_marketing_campaigns.csv"
                        ),
                    }
                )
            )

            # Save the reports to the state
            if result.raw:
                # Store reports with appropriate keys
                self.state.marketing_report = result.raw
                logger.info("Marketing reports generated successfully")
            else:
                logger.error("Failed to generate marketing reports")
        except Exception as e:
            logger.error(f"Error generating marketing reports: {str(e)}", exc_info=True)

    @listen(generate_mkt_ops_reports)
    def display_mkt_ops_report_summaries(self):
        logger.info("Displaying marketing report summaries...")

        # Ensure reports directory exists
        self.state.reports_dir.mkdir(exist_ok=True)

        # Marketing Report
        logger.info("=== MARKETING REPORT SUMMARY ===")
        if self.state.marketing_report:
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(self.state.marketing_report.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            logger.info(f"Report summary: {summary}")

            # Save report to file
            report_path = self.state.reports_dir / "marketing_report.md"
            report_path.write_text(self.state.marketing_report)
            logger.info(f"Complete report saved to {report_path}")
        else:
            logger.warning("No Marketing report content available")
