from __future__ import annotations
from pydantic import BaseModel
from typing import Literal,Optional


class MortgageApplicationCreate(BaseModel):
    annual_income: float
    credit_score: int
    monthly_debt: float
    loan_amount: float
    property_value:float
    employment_status: Literal["employed", "unemployed", "self-employed"]

class UnderWritingDecisionResponse(BaseModel):
    decision: Literal["approved", "denied", "refer"]
    risk_score: int
    reasons: list[str]
    conditions: list[str]
    explanation: dict
    ml_risk_score: Optional[float] = None

    






    





