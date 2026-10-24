from pydantic import BaseModel, Field
from typing import Literal, List



class SupportingEvidence(BaseModel):
    statement: str = Field(description = "Evidence extracted from research")
    source_url: str = Field(description = "source url of the evidence")

class IndustryOutlook(BaseModel):
    outlook: Literal["GROWING", "STABLE", "DECLINING", "INSUFFICIENT EVIDENCE"] = Field(description = "The industry outlook based on recent news articles from recognised sources.")
    rationale: str = Field(description = "Brief reasoning behind the assesment")
    supporting_evidence: List[SupportingEvidence]
    
class IndustryIntelligence(BaseModel):
    industry_outlook: IndustryOutlook