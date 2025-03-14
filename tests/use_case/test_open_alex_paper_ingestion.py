from icecream import ic
from wsl_library.usecase.open_alex_paper_ingestion import OpenAlexPaperIngestionUseCase
# from wsl_library.domain.paper_taxonomy import OpenAlexPaper, PaperWithText

from wsl_library.scraping import extract_openalex as OpenAlexClient
from wsl_library.pdfextraction.llm import ollama_extraction as LlmClient
from wsl_library.pdfextraction.pdf import extract_pdf_content as PDFExtractor
from wsl_library.infra import JSON_STORAGE_FOLDER, PDF_STORAGE_FOLDER

my_instance = OpenAlexPaperIngestionUseCase(
    OpenAlexClient, LlmClient, PDF_STORAGE_FOLDER, PDFExtractor
)

my_instance.ingest_papers_with_query(
    query="construction", limit=2, model="smollm:135m"
    , prompt_type="basic"
    # , prompt_type="main_parts"
)

ic('Hell yeah!')