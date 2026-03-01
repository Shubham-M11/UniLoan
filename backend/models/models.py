from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    loan_type = Column(String) # "Personal" or "Business"
    
    # Common features
    loan_amount = Column(Float)
    term_months = Column(Integer)
    credit_score = Column(Integer)
    income_revenue = Column(Float)
    
    # Personal specific
    existing_emi = Column(Float, nullable=True)
    employment_years = Column(Integer, nullable=True)
    
    # Business specific
    net_profit = Column(Float, nullable=True)
    business_age_years = Column(Integer, nullable=True)
    
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

class PredictionResult(Base):
    __tablename__ = "prediction_results"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, unique=True)
    approval_probability = Column(Float)
    risk_level = Column(String)
    suggested_loan_amount = Column(Float, nullable=True)
    shap_explanation = Column(String) # Stored as JSON string
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
