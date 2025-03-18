from typing import List
from icecream import ic
from wsl_library.domain.paper_taxonomy import OpenAlexPaper, PaperWithText, PaperTaxonomy


class OpenAlexPaperIngestionUseCase:

    def __init__(self, open_alex_client, llm_client, paper_repository, pdf_store):
        self.open_alex_client = open_alex_client
        self.llm_client = llm_client
        self.paper_repository = paper_repository
        self.pdf_store = pdf_store


    def ingest_papers_with_query(self, query: str = "mobility", limit: int = 10, model: str = "smollm:135m", prompt_type: str = "basic"):
        papers_list: List[OpenAlexPaper] = self.open_alex_client.get_papers(
            query_requested=query, limitation=limit
        )
        extracted_text_list: List[PaperWithText] = self.pdf_store.extract_text(papers_list)
        papers_with_taxonomy = []
        for pix, paper in enumerate(extracted_text_list[:2]):
            print(f"Processing paper text to fill taxonomy : {pix + 1}/{len(extracted_text_list)}")
            # TODO : In Pydantic classes : Add the taxonomy to the input object, for enrichment in one entity
            paper_with_taxonomy: PaperTaxonomy = self.llm_client.get_taxonomy_from_paper(paper, model, prompt_type)

            # papers_with_taxonomy.embeddings = self.llm_client.get_embeddings(paper.extract_text)
            papers_with_taxonomy.append(paper_with_taxonomy)
        # self.paper_repository.save_all(papers_with_taxonomy)
        ic(len(papers_with_taxonomy))

