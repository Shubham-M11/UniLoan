from pydantic import BaseModel, Field
from typing import Optional, List

# ----- Personal Loan Schemas -----

class PersonalLoanRequest(BaseModel):
    age: int = Field(..., gt=18, description="Age of applicant")
    income: float = Field(..., gt=0, description="Monthly income in currency")
    emi: float = Field(default=0, ge=0, description="Existing monthly EMIs")
    credit_score: int = Field(..., ge=300, le=850, description="Applicant credit score")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    tenure: int = Field(..., gt=0, description="Loan term in months")

class PersonalLoanResponse(BaseModel):
    approval_probability: float
    risk_level: str
    suggested_loan_amount: float
    key_factors: List[str]
    advisory: str

# ----- Business Loan Schemas -----

class BusinessLoanRequest(BaseModel):
    annual_revenue: float = Field(..., gt=0, description="Annual business revenue")
    net_profit: float = Field(..., description="Annual net profit")
    business_age: int = Field(..., ge=0, description="Age of business in years")
    existing_liabilities: float = Field(default=0, ge=0, description="Total existing liabilities")
    credit_score: int = Field(..., ge=300, le=850, description="Business credit score")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    tenure: int = Field(..., gt=0, description="Loan term in months")

class BusinessLoanResponse(BaseModel):
    approval_probability: float
    risk_level: str
    suggested_loan_amount: float
    key_factors: List[str]
    advisory: str
