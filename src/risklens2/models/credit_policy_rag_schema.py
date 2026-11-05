from pydantic import BaseModel, Field
from typing import List

class Source(BaseModel):
    pages: List[int] = Field(description = "page numbers for the output source.")
    section: str = Field(description = "Which section from the knowledge source the answer comes from")
    source_doc: str = Field(..., description = "Name of the source document. ")
    chunk_id: str = Field(description = "chunk id for the relevant chunk")

class RAGResponse(BaseModel):
    answer: str = Field(..., description = "Answer from the llm for user's query")
    sources: List[Source]
