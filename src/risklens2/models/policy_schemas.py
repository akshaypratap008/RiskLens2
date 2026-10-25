from pydantic import BaseModel, Field
from typing import Literal

class PolicyRuleResult(BaseModel):
    rule_name: str = Field(..., description="Financial Ratios checked against the credit polciy")
    status: Literal['pass', 'fail'] = Field(..., description = "Did the assesed rule based on the policy passed or fail")
    message: str = Field(description= "The message based on the assesment")

class PolicyAssessment(BaseModel):
    passed_rules: list[PolicyRuleResult]
    failed_rules: list[PolicyRuleResult]
    recomendation : Literal["APPROVE", "DECLINE", "REFER"] = Field(..., description = "Final recomendation based on number for failed metrics.")

