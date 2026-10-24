from pydantic import BaseModel, Field
from typing import Literal, List

# models used by key component models
class SupportingEvidence(BaseModel):
    statement: str = Field(description = "Evidence extracted from research")
    source_url: str = Field(description = "source url of the evidence")

class SenstivityModel(BaseModel):
    sensitivity: Literal["HIGH", "MEDIUM", "LOW", "INSUFFICIENT_EVIDENCE"]
    rationale: str = Field(description = "Brief reasoning behind the assesment")
    supporting_evidence: List[SupportingEvidence]

class RiskModel(BaseModel):
    risk: str = Field(description = "The kind of risk present")
    rationale: str = Field(description = "Brief reasoning behind the assesment")
    supporting_evidence : List[SupportingEvidence]

# key components 
class IndustryOutlook(BaseModel):
    outlook: Literal["GROWING", "STABLE", "DECLINING", "INSUFFICIENT EVIDENCE"] = Field(description = "The industry outlook based on recent news articles from recognised sources.")
    rationale: str = Field(description = "Brief reasoning behind the assesment")
    supporting_evidence: List[SupportingEvidence]

class KeyIndustryRisks(BaseModel):
    key_industry_risks: List[RiskModel]
    
class InsolvencyTrend(BaseModel):
    insolvency_trend: Literal["INCREASING", "STABLE", "DECREASING", "INSUFFICIENT_EVIDENCE"]
    rationale: str = Field(description = "Brief reasoning behind the assesment")
    supporting_evidence: List[SupportingEvidence]

class RegulatoryRisks(BaseModel):
    regulatory_risk: Literal["HIGH", "MEDIUM", "LOW", "INSUFFICIENT_EVIDENCE"]
    rationale: str = Field(description = "Brief reasoning behind the assesment")
    supporting_evidence: List[SupportingEvidence]

class MacroeconomicSentivity(BaseModel):
    interest_rates: SenstivityModel
    inflation: SenstivityModel
    consumer_spending: SenstivityModel
    energy_prices: SenstivityModel

# final output
class IndustryIntelligence(BaseModel):
    industry_name: str 
    industry_outlook: IndustryOutlook
    key_industry_risks: KeyIndustryRisks
    insolvency_trends: InsolvencyTrend
    regulatory_risks: RegulatoryRisks
    macroeconomic_senstivity: MacroeconomicSentivity