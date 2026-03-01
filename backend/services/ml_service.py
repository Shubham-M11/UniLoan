import os
import joblib
import pandas as pd
import numpy as np

# Adjust paths relative to this file
base_dir = os.path.dirname(os.path.dirname(__file__))
pipeline_path = os.path.join(base_dir, 'ml', 'loan_model_pipeline.pkl')
columns_path = os.path.join(base_dir, 'ml', 'training_columns.pkl')

pipeline = None
training_columns = None

try:
    pipeline = joblib.load(pipeline_path)
    training_columns = joblib.load(columns_path)
    print("Loaded ML pipeline successfully.")
except Exception as e:
    print(f"Warning: Could not load ML pipeline. Generating dummy predictions. Error: {e}")

def get_base_features(data: dict, is_business: bool):
    # Mapping Personal/Business API inputs to the Kaggle Dataset features
    
    # Convert INR input to a scale comparable to the US training data.
    # A simple exchange rate conversion (÷83) makes Indian incomes look 
    # extremely low ($14K vs training median of $67K). We use a Purchasing
    # Power Parity (PPP) multiplier to properly scale: $1 in India buys
    # roughly 4.5x what $1 buys in the US (World Bank PPP factor).
    exchange_rate = 83.0
    ppp_multiplier = 4.5  # PPP adjustment for India vs US
    
    # Tenure in months (default 12)
    tenure_months = data.get('tenure', 12)
    tenure_years = max(tenure_months / 12, 1)
    
    if not is_business:
        # Personal: income is monthly INR, convert to annual PPP-adjusted USD
        income = (data.get('income', 50000) / exchange_rate) * 12 * ppp_multiplier
        loan_amnt = data.get('loan_amount', 500000) / exchange_rate * ppp_multiplier
    else:
        # Business: annual_revenue is already annual INR
        income = data.get('annual_revenue', 1000000) / exchange_rate * ppp_multiplier
        loan_amnt = data.get('loan_amount', 500000) / exchange_rate * ppp_multiplier
    
    # Use annual loan burden (loan spread over tenure) vs annual income
    annual_loan_burden = loan_amnt / tenure_years
    percent_income = annual_loan_burden / income if income > 0 else 0
    
    # Clamp features to the training data's observed ranges to prevent
    # out-of-distribution predictions (model was trained on these ranges):
    #   person_income: [8,000 - 200,000]  (annual USD)
    #   loan_amnt:     [500 - 35,000]     (USD)
    #   loan_percent_income: [0 - 0.66]
    income = max(8000, min(income, 200000))
    loan_amnt = max(500, min(loan_amnt, 35000))
    percent_income = min(percent_income, 0.66)
    
    # Age: use user's actual age for personal, default 40 for business
    age = data.get('age', 35) if not is_business else 40
    
    return {
        'person_age': age,
        'person_gender': 'female', # Not collected in form, setting default
        'person_education': 'Bachelor',
        'person_income': income,
        'person_emp_exp': data.get('business_age', 5) if is_business else 3,
        'person_home_ownership': 'RENT' if not is_business else 'OWN',
        'loan_amnt': loan_amnt,
        'loan_intent': 'VENTURE' if is_business else 'PERSONAL',
        'loan_int_rate': 12.0 if not is_business else 15.0,
        'loan_percent_income': percent_income,
        'cb_person_cred_hist_length': 5 if not is_business else 10,
        'credit_score': data.get('credit_score', 650),
        'previous_loan_defaults_on_file': 'No'
    }

def get_prediction_and_explanation(input_data: dict, is_business: bool):
    if pipeline is None:
        # Fallback to dummy
        prob = 0.8
        risk = "Low"
        return {
            "approval_probability": 0.8,
            "risk_level": "Low",
            "suggested_loan_amount": input_data.get('loan_amount', 0),
            "key_factors": ["High credit score", "Stable income"],
            "advisory": "Maintain good credit history."
        }
        
    features = get_base_features(input_data, is_business)
    df = pd.DataFrame([features])
    
    # Predict Approval (1 = Approved, 0 = Rejected)
    try:
        if hasattr(pipeline, "predict_proba"):
            prob = pipeline.predict_proba(df)[0][1]
        else:
            prob = pipeline.predict(df)[0]
    except Exception as e:
        print("Prediction Error:", e)
        prob = 0.5
        
    # prob is Probability of Default (1 = Default)
    approval_prob = 1.0 - prob
        
    risk = "Low" if approval_prob > 0.65 else "Medium" if approval_prob > 0.4 else "High"
    
    # Since extracting strict SHAP values from a pipeline requires manual unpacking of transformers,
    # we will dynamically generate the key factors based on the raw rules the model learns.
    
    factors = []
    
    # Non-technical credit score explanation
    if features['credit_score'] >= 720:
        factors.append("You have a great credit score, which shows you manage your finances very well.")
    elif features['credit_score'] >= 600:
        factors.append("Your credit score is fair, but there's still a bit of room for improvement.")
    else:
        factors.append("Your credit score is on the lower side. Improving it could really boost your chances of approval.")
        
    # Non-technical debt-to-income explanation
    if features['loan_percent_income'] > 0.4:
        factors.append("The loan amount you want is quite large compared to your income. Asking for a smaller amount might help.")
    else:
        factors.append("The loan amount you've requested is very reasonable compared to what you earn.")
        
    # Non-technical business experience explanation
    if is_business and features.get('person_emp_exp', 0) > 3:
        factors.append("Your business has been operating for a few years, which brings solid stability to your application.")
        
    # Dynamic Suggestion: Max 30% of annual income directed to loan payments
    tenure_months = input_data.get('tenure', 12)
    tenure_years = max(tenure_months / 12, 1)
    
    if not is_business:
        annual_inr = input_data.get('income', 50000) * 12
    else:
        annual_inr = input_data.get('annual_revenue', 1000000)
        
    safe_annual_payment = annual_inr * 0.30
    safe_total_loan = safe_annual_payment * tenure_years
    
    req_loan = input_data.get('loan_amount', 100000)
    
    if risk == "Low":
        suggestion = req_loan
    else:
        # Suggest safe amount based on income, or just a slight 10% reduction if it's already safe but credit is poor
        suggestion = min(req_loan * 0.9, safe_total_loan)
        
    # Dynamic, simple advisory based on risk level
    if risk == "Low":
        advisory = "Great news! Your profile looks very strong, and you have excellent chances of getting this loan."
    elif risk == "Medium":
        advisory = "You have a fair chance of approval. You could improve your odds by requesting a slightly smaller loan amount or paying off some existing debts."
    else:
        advisory = "Currently, your application might be considered high risk. We recommend working on improving your credit score or reducing the loan amount you're asking for."
        
    return {
        "approval_probability": round(float(approval_prob) * 100) / 100,
        "risk_level": risk,
        "suggested_loan_amount": float(suggestion),
        "key_factors": factors,
        "advisory": advisory
    }

def predict_personal_loan(data: dict):
    return get_prediction_and_explanation(data, is_business=False)

def predict_business_loan(data: dict):
    return get_prediction_and_explanation(data, is_business=True)
