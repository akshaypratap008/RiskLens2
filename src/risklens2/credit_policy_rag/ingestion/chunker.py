from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.document import DoclingDocument
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.chunking import HierarchicalChunker, HybridChunker

import uuid
from pathlib import Path
import yaml

CREDIT_POLICY_FILE_PATH = "data/credit_policy_extract_2.pdf"
RAG_CONFIG_FILE_PATH = Path(__file__).parents[1] / "rag_config.yaml"
with open(RAG_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

PIPELINE_OPTIONS = PdfPipelineOptions()
PIPELINE_OPTIONS.do_ocr = False
PIPELINE_OPTIONS.generate_page_images = False
PIPELINE_OPTIONS.generate_picture_images = False
PIPELINE_OPTIONS.do_table_structure = True

class CreditPolicyChunker:
    """Responsible for chunking the credit policy document. Uses docling chunker to retain the tables"""

    def __init__(self):
        self.converter = DocumentConverter(
            format_options={
                "pdf": PdfFormatOption(
                    pipeline_options = PIPELINE_OPTIONS
                )
            }
        )
        self.chunking_config = config["rag"]["chunker"]["hybrid"]
        self.chunker = HybridChunker(
            max_tokens = self.chunking_config["max_tokens"],
            merge_peers = self.chunking_config["merge_peers"],
            repeat_table_header = self.chunking_config["repeat_table_header"]
        )

    def convert_to_doc(self, CREDIT_POLICY_FILE_PATH) -> DoclingDocument:
        self.file_path = CREDIT_POLICY_FILE_PATH

        result = self.converter.convert(self.file_path)
        docling_doc = result.document

        return docling_doc

    def create_chunks(self, doc) -> list:
        if isinstance(doc, DoclingDocument):
            doc_chunks = self.chunker.chunk(doc)
        else:
            doc_chunks = doc  # Cached DocChunk objects; don't chunk them again.
        chunks = []

        for chunk in doc_chunks:
            content = self.chunker.contextualize(chunk)
            metadata = self._get_chunk_metadata(chunk = chunk)

            chunks.append({
                "content": content,
                "metadata": metadata
            })

        return chunks

    def _get_chunk_metadata(self, chunk) -> dict:
        metadata = {
            "chunk_id": str(uuid.uuid4()),
            "document_name": chunk.meta.origin.filename,
            "section": chunk.meta.headings or [],
            "pages": self._extract_page_no(chunk = chunk),
            "content_type": self._extract_chunk_type(chunk = chunk)
        }
        return metadata

    def _extract_page_no(self, chunk) -> list:
        pages = []
        for item in chunk.meta.doc_items:
            for prov in item.prov:
                if prov.page_no not in pages:
                    pages.append(prov.page_no)

        return pages
    
    def _extract_chunk_type(self, chunk) -> str:
        labels = {
            item.label.value for item in chunk.meta.doc_items
        }

        if "table" in labels:
            return "table"

        if "list_item" in labels:
            return "list"

        if "text" in labels:
            return "text"

        if "section_header" in labels:
            return "heading"

        return "other"

    def _extract_element_types(self, chunk) -> list[str]:
        return sorted({
            item.label.value
            for item in chunk.meta.doc_items
        })
        

    
    
    