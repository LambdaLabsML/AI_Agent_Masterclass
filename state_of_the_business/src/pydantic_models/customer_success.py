from pydantic import BaseModel
from pathlib import Path


class CustomerSuccessOpsState(BaseModel):
    """State containing all the data and reports for customer success operations."""

    datasets_dir: Path = Path(__file__).parent.parent.parent / "datasets"
    reports_dir: Path = Path(__file__).parent.parent.parent / "reports"
    customer_success_report: str = ""
