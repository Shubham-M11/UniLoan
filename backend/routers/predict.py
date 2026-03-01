from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import LoanApplication, PredictionResult
from schemas.schemas import PersonalLoanRequest, PersonalLoanResponse, BusinessLoanRequest, BusinessLoanResponse
from services import ml_service

router = APIRouter()

@router.post("/personal", response_model=PersonalLoanResponse)
def predict_personal(request: PersonalLoanRequest, db: Session = Depends(get_db)):
    # 1. Save application to DB
    application = LoanApplication(
        loan_type="Personal",
        loan_amount=request.loan_amount,
        term_months=request.tenure,
        credit_score=request.credit_score,
        income_revenue=request.income,
        existing_emi=request.emi
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    
    # 2. Call ML Service
    prediction = ml_service.predict_personal_loan(request.dict())
    
    # 3. Save Prediction Result to DB
    result = PredictionResult(
        application_id=application.id,
        approval_probability=prediction["approval_probability"],
        risk_level=prediction["risk_level"],
        suggested_loan_amount=prediction["suggested_loan_amount"]
    )
    db.add(result)
    db.commit()
    
    return prediction

@router.post("/business", response_model=BusinessLoanResponse)
def predict_business(request: BusinessLoanRequest, db: Session = Depends(get_db)):
    # 1. Save application to DB
    application = LoanApplication(
        loan_type="Business",
        loan_amount=request.loan_amount,
        term_months=request.tenure,
        credit_score=request.credit_score,
        income_revenue=request.annual_revenue,
        net_profit=request.net_profit
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    
    # 2. Call ML Service
    prediction = ml_service.predict_business_loan(request.dict())
    
    # 3. Save Prediction Result to DB
    result = PredictionResult(
        application_id=application.id,
        approval_probability=prediction["approval_probability"],
        risk_level=prediction["risk_level"],
        suggested_loan_amount=prediction["suggested_loan_amount"]
    )
    db.add(result)
    db.commit()
    
    return prediction
