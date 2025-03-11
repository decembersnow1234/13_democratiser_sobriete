from src.wsl_library.usecase.open_alex_paper_ingestion import OpenAlexPaperIngestionUseCase
# from src.wsl_library.domain.paper_taxonomy import OpenAlexPaper, PaperWithText

from src.wsl_library.scraping import extract_openalex as OpenAlexClient
from src.wsl_library.pdfextraction.llm import ollama_extraction as LlmClient
from src.wsl_library.infra import JSON_STORAGE_FOLDER, PDF_STORAGE_FOLDER

my_instance = OpenAlexPaperIngestionUseCase(
    OpenAlexClient, LlmClient, JSON_STORAGE_FOLDER, PDF_STORAGE_FOLDER
)
