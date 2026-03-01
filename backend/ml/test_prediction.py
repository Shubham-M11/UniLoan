import pandas as pd
import joblib
import os
import sys

# Load model pipeline
base_dir = os.path.dirname(__file__)
pipeline_path = os.path.join(base_dir, 'loan_model_pipeline.pkl')
columns_path = os.path.join(base_dir, 'training_columns.pkl')

pipeline = joblib.load(pipeline_path)
training_cols = joblib.load(columns_path)

print("Pipeline loaded.")

def predict(features):
    # Ensure column order matches training
    df = pd.DataFrame([features])
    
    # Check if there are missing columns
    for col in training_cols:
        if col not in df.columns:
            print(f"Warning: {col} missing from features")
            df[col] = 0
            
    df = df[training_cols]  # Enforce column order

    if hasattr(pipeline, "predict_proba"):
        prob = pipeline.predict_proba(df)[0][1]
    else:
        prob = pipeline.predict(df)[0]
    return prob

input1 = {
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

input2 = {
    'person_age': 45,
    'person_gender': 'male',
    'person_education': 'Master',
    'person_income': 150000,
    'person_emp_exp': 15,
    'person_home_ownership': 'OWN',
    'loan_amnt': 5000,
    'loan_intent': 'VENTURE',
    'loan_int_rate': 5.0,
    'loan_percent_income': 5000 / 150000,
    'cb_person_cred_hist_length': 15,
    'credit_score': 800,
    'previous_loan_defaults_on_file': 'No'
}

print(f"Prediction 1 (High Risk): {predict(input1)}")
print(f"Prediction 2 (Low Risk): {predict(input2)}")
