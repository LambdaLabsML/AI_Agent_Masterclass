import logging
from pathlib import Path
from llama_index.readers.file import CSVReader
from src.utils.logging_config import logger

# Get logger for this module
logger = logging.getLogger(__name__)


def validate_csv_files():
    """
    Validate all CSV files in the datasets directory.
    """

    logger.info("Starting company data validation...")

    # get all csv files
    datasets_dir = Path(__file__).parent.parent.parent / "datasets"
    csv_files = list(datasets_dir.glob("*.csv"))

    for fp in csv_files:
        if not fp.exists():
            error_msg = f"Required file not found: {fp}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            # Use LlamaIndex's CSVReader
            reader = CSVReader()
            documents = reader.load_data(file=fp)

            if not documents or len(documents) == 0:
                logger.error(f"Empty or malformed data in {fp}")
            else:
                logger.info(f"Successfully validated {fp}")
                logger.info(f"Found {len(documents)} rows of data")
        except Exception as e:
            logger.error(f"Failed to validate {fp} data: {str(e)}", exc_info=True)
            raise
