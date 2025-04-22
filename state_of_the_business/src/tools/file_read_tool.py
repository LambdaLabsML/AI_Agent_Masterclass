from crewai_tools import FileReadTool


class DatasetFileReadTool(FileReadTool):
    """A tool for reading files in the datasets directory."""

    def __init__(self):
        """Initialize the tool without a specific file path."""
        super().__init__()

    def set_file_path(self, file_path: str):
        """Set the file path to read.

        Args:
            file_path (str): Path to the file to read
        """
        self._file_path = file_path
