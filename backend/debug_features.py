import json
from services.ml_service import get_base_features, get_prediction_and_explanation

# Check what features are generated for a typical healthy personal loan
personal_input = {'age': 35, 'income': 100000, 'emi': 0, 'credit_score': 750, 'loan_amount': 500000, 'tenure': 24}
features = get_base_features(personal_input, False)
print("=== Features sent to model ===")
print(json.dumps(features, indent=2))

# Check prediction
result = get_prediction_and_explanation(personal_input, False)
print("\n=== Prediction Result ===")
print(json.dumps(result, indent=2))

# Now test with a known-good direct input that we know works
import pandas as pd
import joblib
pipeline = joblib.load('ml/loan_model_pipeline.pkl')

# This was verified to produce 0.008 default prob
direct_input = {
    'person_age': 25,
    'person_gender': 'female',
    'person_education': 'Bachelor',
    'person_income': 30000,
    'person_emp_exp': 1,
    'person_home_ownership': 'RENT',
    'loan_amnt': 20000,
    'loan_intent': 'PERSONAL',
    'loan_int_rate': 20.0,
    'loan_percent_income': 20000 / 30000,
    'cb_person_cred_hist_length': 1,
    'credit_score': 500,
    'previous_loan_defaults_on_file': 'Yes'
}
df_direct = pd.DataFrame([direct_input])
print("\n=== Direct model prediction (known risky) ===")
print(pipeline.predict_proba(df_direct)[0])

# Now test with the features from the service  
df_service = pd.DataFrame([features])
print("\n=== Service features prediction ===")
print(pipeline.predict_proba(df_service)[0])
