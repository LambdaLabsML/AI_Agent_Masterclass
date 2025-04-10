#!/usr/bin/env python
import os
import asyncio
import csv
from pathlib import Path
from typing import Dict

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from .crews.sales_ops_crew.sales_ops_crew import SalesOpsCrew


class SalesOpsState(BaseModel):
    """State containing all the data and reports for sales operations."""
    datasets_dir: Path = Path(__file__).parent.parent.parent / "datasets"
    reports: Dict[str, str] = {}

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
    def generate_sales_reports(self):
        print("\n--- Generating Sales Reports ---")
        
        # Create the sales ops crew
        sales_ops_crew = SalesOpsCrew().crew()
        
        # Start the crew
        result = sales_ops_crew.kickoff(
            inputs={
                "month": "03",
                "year": "2025",
                "direct_sales_data": str(self.state.datasets_dir / "spaceoutfitters_sales.csv"),
                "b2b_sales_data": str(self.state.datasets_dir / "spaceoutfitters_b2b_sales.csv"),
            }
        )

        # Get reports from the task outputs
        try:
            # Access the outputs from each task
            b2c_task = sales_ops_crew.tasks[0]  # First task (B2C report)
            b2b_task = sales_ops_crew.tasks[1]  # Second task (B2B report)
            
            # Store reports in state
            self.state.reports = {
                "direct_sales": b2c_task.output.raw_output if hasattr(b2c_task, 'output') else "",
                "b2b_sales": b2b_task.output.raw_output if hasattr(b2b_task, 'output') else ""
            }
            
            print(f"✅ Sales reports generated")
            print(f"Reports available: {list(self.state.reports.keys())}")
        except Exception as e:
            print(f"⚠️ Error accessing task outputs: {str(e)}")
            # Fallback to the raw result if available
            if result and hasattr(result, 'raw'):
                self.state.reports = {"combined_report": result.raw}
                print(f"✅ Saved combined report as fallback")
            else:
                print(f"⚠️ Unable to generate sales reports")

    @listen(generate_sales_reports)
    def display_report_summaries(self):
        print("\n--- Report Summaries ---")

        for report_type, report_content in self.state.reports.items():
            print(f"\n=== {report_type.upper()} REPORT SUMMARY ===")
            # Display first 10 lines or 500 characters, whichever is shorter
            summary = "\n".join(report_content.split("\n")[:10])
            if len(summary) > 500:
                summary = summary[:497] + "..."
            print(summary)
            print(f"Complete report saved to reports/{report_type}_report.md")
    
    def print_full_reports(self):
        """Print the full content of all reports"""
        print("\n" + "="*50)
        print("===== FULL REPORTS =====")
        print("="*50)
        
        for report_type, report_content in self.state.reports.items():
            print(f"\n{'='*20} {report_type.upper()} FULL REPORT {'='*20}\n")
            print(report_content)
            print("\n" + "="*80 + "\n")


def kickoff():
    print("\n🚀 Starting Sales Operations Flow\n")
    sales_ops_flow = SalesOpsFlow()
    result = sales_ops_flow.kickoff()
    
    # Print full reports after flow completion if reports were generated
    if hasattr(sales_ops_flow.state, 'reports') and sales_ops_flow.state.reports:
        sales_ops_flow.print_full_reports()
    
    print("\n✅ Sales Operations Flow completed successfully!\n")
    return result


def plot():
    sales_ops_flow = SalesOpsFlow()
    sales_ops_flow.plot()


if __name__ == "__main__":
    kickoff()
