#!/usr/bin/env python
import os
import asyncio
import csv
from pathlib import Path
from typing import Dict

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from .crews.sales_ops_B2C_crew.sales_ops_b2c_crew import SalesOpsB2CCrew
from .crews.sales_ops_B2B_crew.sales_ops_b2b_crew import SalesOpsB2BCrew


class SalesOpsState(BaseModel):
    """State containing all the data and reports for sales operations."""

    datasets_dir: Path = Path(__file__).parent.parent.parent / "datasets"
    reports_dir: Path = Path(__file__).parent.parent.parent / "reports"
    b2c_report: str = ""
    b2b_report: str = ""


class SalesOpsFlow(Flow[SalesOpsState]):

    @start()
    def validate_company_data(self):
        print("Verifying company data integrity...")

        # Get the path to CSV files in the datasets directory
        dataset_dir = self.state.datasets_dir

        # Find all CSV files in the datasets directory
        csv_files = {}
        for csv_path in dataset_dir.glob("*.csv"):
            # Use filename without extension as the key
            key = csv_path.stem
            csv_files[key] = csv_path

        if not csv_files:
            print("⚠️ Warning: No CSV files found in datasets directory")

        # Verify integrity of all CSV files
        for key, file_path in csv_files.items():
            if not file_path.exists():
                print(f"⚠️ Warning: {file_path} not found")
                continue

            try:
                with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                    # Attempt to parse CSV to verify integrity
                    csv_reader = csv.reader(file)
                    # Read header
                    header = next(csv_reader, None)
                    # Verify at least one row of data exists
                    first_row = next(csv_reader, None)

                    if not header or not first_row:
                        print(f"⚠️ Error: {key} data is empty or malformed")
                    else:
                        print(f"✅ Verified {key} data integrity at {file_path}")
            except Exception as e:
                print(f"⚠️ Error: Failed to validate {key} data: {str(e)}")

    @listen(validate_company_data)
    def generate_b2c_sales_reports(self):
        print("\n--- Generating Sales Reports ---")

        # Start crew Sales report
        result = (
            SalesOpsB2CCrew()
            .crew()
            .kickoff(
                inputs={
                    "month": "03",
                    "year": "2025",
                    "b2c_sales_data": str(
                        self.state.datasets_dir / "spaceoutfitters_sales.csv"
                    ),
                }
            )
        )

        # Save the reports to the state
        if result.raw:
            # Store reports with appropriate keys
            self.state.b2c_report = result.raw

            print(f"✅ Sales reports generated")
            print(self.state.b2c_report)
        else:
            print(f"⚠️ Unable to generate sales reports")

    @listen(generate_b2c_sales_reports)
    def display_report_summaries(self):
        print("\n--- Report Summaries ---")

        # Ensure reports directory exists
        self.state.reports_dir.mkdir(exist_ok=True)

        # B2C Report
        print("\n=== B2C REPORT SUMMARY ===")
        if self.state.b2c_report:
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(self.state.b2c_report.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            print(summary)

            # Save report to file
            report_path = self.state.reports_dir / "b2c_report.md"
            report_path.write_text(self.state.b2c_report)
            print(f"Complete report saved to {report_path}")
        else:
            print("No B2C report content available.")

    @listen(generate_b2c_sales_reports)
    def generate_b2b_sales_reports(self):
        print("\n--- Generating Sales Reports ---")

        # Start crew Sales report
        result = (
            SalesOpsB2BCrew()
            .crew()
            .kickoff(
                inputs={
                    "month": "03",
                    "year": "2025",
                    "b2b_sales_data": str(
                        self.state.datasets_dir / "spaceoutfitters_b2b_sales.csv"
                    ),
                }
            )
        )

        # Save the reports to the state
        if result.raw:
            # Store reports with appropriate keys
            self.state.b2b_report = result.raw

            print(f"✅ Sales reports generated")
            print(self.state.b2b_report)
        else:
            print(f"⚠️ Unable to generate sales reports")

    @listen(generate_b2b_sales_reports)
    def display_b2b_report_summaries(self):
        print("\n--- Report Summaries ---")

        # Ensure reports directory exists
        self.state.reports_dir.mkdir(exist_ok=True)

        # B2B Report
        print("\n=== B2B REPORT SUMMARY ===")
        if self.state.b2b_report:
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(self.state.b2b_report.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            print(summary)

            # Save report to file
            report_path = self.state.reports_dir / "b2b_report.md"
            report_path.write_text(self.state.b2b_report)
            print(f"Complete report saved to {report_path}")
        else:
            print("No B2B report content available.")


def kickoff():
    print("\n🚀 Starting Sales Operations Flow\n")
    sales_ops_flow = SalesOpsFlow()
    result = sales_ops_flow.kickoff()
    print("\n✅ Sales Operations Flow completed successfully!\n")
    return result


def plot():
    sales_ops_flow = SalesOpsFlow()
    sales_ops_flow.plot()


if __name__ == "__main__":
    kickoff()
