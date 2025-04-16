from pydantic import BaseModel
from pathlib import Path


class SalesOpsState(BaseModel):
    """State containing all the data and reports for sales operations."""

    datasets_dir: Path = Path(__file__).parent.parent.parent / "datasets"
    reports_dir: Path = Path(__file__).parent.parent.parent / "reports"
    b2c_report: str = ""
    b2b_report: str = ""
