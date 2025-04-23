from crewai.tools import BaseTool
from llama_index.readers.file import CSVReader



class LlamaCSVFileReadTool(BaseTool):
    name: str = "LlamaIndex CSV Tool"
    description: str = "Uses LlamaIndex to read and parse a CSV file"

    def _run(self, file_path: str) -> str:
        reader = CSVReader()
        documents = reader.load_data(file_path)
        return "\n".join([doc.text for doc in documents])
