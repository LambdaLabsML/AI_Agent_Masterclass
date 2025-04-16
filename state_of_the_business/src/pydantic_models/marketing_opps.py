from pydantic import BaseModel
from pathlib import Path


class MarketingOpsState(BaseModel):
    """State containing all the data and reports for marketing operations."""

    datasets_dir: Path = Path(__file__).parent.parent.parent / "datasets"
    reports_dir: Path = Path(__file__).parent.parent.parent / "reports"
    marketing_report: str = ""
