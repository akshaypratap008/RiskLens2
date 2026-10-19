from pydantic import BaseModel, Field
from typing import Literal

class CompanyProfile(BaseModel):
    company_number: str = Field(..., description="Company's registration number")
    company_name: str = Field(description = "Company's legal name")
    company_status: str = Field(description = "Status of the company on the companies house. Active or Dissolved")