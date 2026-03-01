import pandas as pd
import joblib
import json

pipeline = joblib.load('ml/loan_model_pipeline.pkl')

# Base features from the service (healthy profile)
base = {
    'person_age': 35,
    'person_gender': 'female',
    'person_education': 'Bachelor',
    'person_income': 14457.83,
    'person_emp_exp': 3,
    'person_home_ownership': 'RENT',
    'loan_amnt': 6024.10,
    'loan_intent': 'PERSONAL',
    'loan_int_rate': 12.0,
    'loan_percent_income': 0.21,
    'cb_person_cred_hist_length': 5,
    'credit_score': 750,
    'previous_loan_defaults_on_file': 'No'
}

# Test each feature's impact by varying one at a time
print("=== Feature Sensitivity (Default Probability) ===\n")

# Baseline
df = pd.DataFrame([base])
prob = pipeline.predict_proba(df)[0][1]
print(f"Baseline: {prob:.4f}")

# Vary income
for inc in [14000, 30000, 50000, 80000, 100000]:
    test = base.copy()
    test['person_income'] = inc
    test['loan_percent_income'] = test['loan_amnt'] / test['person_income']
    df = pd.DataFrame([test])
    prob = pipeline.predict_proba(df)[0][1]
    print(f"  income={inc:>8}: default_prob={prob:.4f}, pct_inc={test['loan_percent_income']:.3f}")

print()
# Vary loan_amnt  
for amt in [1000, 3000, 6000, 10000, 20000]:
    test = base.copy()
    test['loan_amnt'] = amt
    test['loan_percent_income'] = test['loan_amnt'] / test['person_income']
    df = pd.DataFrame([test])
    prob = pipeline.predict_proba(df)[0][1]
    print(f"  loan_amnt={amt:>6}: default_prob={prob:.4f}, pct_inc={test['loan_percent_income']:.3f}")

print()
# Vary interest rate
for rate in [5, 8, 10, 12, 15, 20]:
    test = base.copy()
    test['loan_int_rate'] = rate
    df = pd.DataFrame([test])
    prob = pipeline.predict_proba(df)[0][1]
    print(f"  int_rate={rate:>5}: default_prob={prob:.4f}")

print()
# Vary credit score
for cs in [500, 600, 650, 700, 750, 800]:
    test = base.copy()
    test['credit_score'] = cs
    df = pd.DataFrame([test])
    prob = pipeline.predict_proba(df)[0][1]
    print(f"  credit_score={cs}: default_prob={prob:.4f}")

print()
# Vary home ownership
for ho in ['RENT', 'OWN', 'MORTGAGE', 'OTHER']:
    test = base.copy()
    test['person_home_ownership'] = ho
    df = pd.DataFrame([test])
    prob = pipeline.predict_proba(df)[0][1]
    print(f"  home={ho:>10}: default_prob={prob:.4f}")

print()
# Vary loan intent
for intent in ['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION']:
    test = base.copy()
    test['loan_intent'] = intent
    df = pd.DataFrame([test])
    prob = pipeline.predict_proba(df)[0][1]
    print(f"  intent={intent:>20}: default_prob={prob:.4f}")
