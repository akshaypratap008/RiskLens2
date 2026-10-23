from pydantic import BaseModel, Field
from typing import Literal

class CompanyAdverseMedia(BaseModel):
    flag_type: Literal["fraud_flag", "insolvency_flag", "legal_flag", "regulatory_flag"] = Field(description="The flag type which has been raised after the news search")
    jev_score: float = Field(..., description= "confidence score of jev when classifying a news article about a company to contain a particular flag", ge=0, le=1)
    url: str = Field(description= "The url of the news source")
    published_date: str | None = Field(default=None, description="Publication date of the news source")
    tavily_search_confidence: float = Field(description= "confidence score of tavily when searching for news about a company", ge=0, le=1)

class DirectorAdverseMedia(BaseModel):
    director_name: str = Field(..., description = "The name of the director the news relates to.")
    flag_type: Literal['fraud_flag', "disqualification_flag", "legal_flag"] = Field(description = "The kind of flag which is raised about the director")
    jev_score: float = Field(..., description= "confidence score of jev when classifying a news article about a director to contain a particular flag", ge=0, le=1)
    url: str = Field(description= "The url of the news source")
    published_date: str | None = Field(default=None, description="Publication date of the news source")
    tavily_search_confidence: float = Field(description= "confidence score of tavily when searching for news about a director", ge=0, le=1)


class AdverseMediaInfo(BaseModel):
    company_adverse_media: list[CompanyAdverseMedia]
    director_adverse_media: list[DirectorAdverseMedia]