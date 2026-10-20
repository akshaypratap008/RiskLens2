from pydantic import BaseModel, Field
from typing import Dict, Optional, Any
from datetime import datetime

class CompanyResearch(BaseModel):
    pass


class CompanyProfile(BaseModel):
    company_name: str = Field(..., description = "Company's legal name")
    company_number: str = Field(..., description="Company's registration number")
    status: str = Field(..., description = "Status of the company on the companies house. Active or Dissolved")
    incorporation_date: datetime = Field(description="Date the company was incorporated")
    age: int = Field(description="Number of years since incorporation")
    type: str = Field(description = "Company type. Example Ltd or partnership")
    sic_code: list = Field(description= "All the SIC codes associated with the company")
    reg_address: dict = Field(description= "Registered Address of the company")
    next_confirmation_statement_due: datetime = Field(description="Next confirmation statement due date")

class DirectorInfo(BaseModel):
    directors: list[Dict[str, Any]] = Field(description= "List of dicts containing info about all the directors")
    secretary: list[Dict[str, Any]] = Field(description= "List of dicts containing info about all the secretary")
    others: list[Dict[str, Any]] = Field(description= "List of dicts containing info about other officiers")
    director_count: int = Field(description= "Total number of directors")
    total_officials: int = Field(description = "Total number of listed officials")
    avg_director_tenure: float = Field(description = "Average tenure of the directors")

class PSCInfo(BaseModel):
    psc_type: str = Field(description = "The type of PSC (individual or corporate)")
    psc_name: Optional[str] = Field(default = None, description="Name of the psc")
    psc_ceased: bool = Field(default = None, description="Is psc active")

    psc_shareholding_band: Optional[str] = Field(default = None, description = "The shareholding bank ('25% to 50%', '50% to 75%', '75% above')")
    psc_voting_rights_band: Optional[str] = Field(default = None, description="Voting rights of the psc. Examples: '25% to 50%', '50% to 75%'")
    psc_right_to_add_remove_director: bool = Field(default = False, description = "Does the psc have right to appoint or remove directors")

    psc_reg_number: Optional[str] = Field(default = None, description = "Registration number of the company in case of corporate psc")
    psc_reg_country: Optional[str] = Field(default = None, description = "Country the psc is registered in if psc is corporate entity")
