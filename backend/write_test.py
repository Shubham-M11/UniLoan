import json
from services.ml_service import predict_personal_loan, predict_business_loan

profiles = {
    'healthy_personal': predict_personal_loan({
        'age': 35, 'income': 100000, 'emi': 0, 'credit_score': 750, 'loan_amount': 500000, 'tenure': 24
    }),
    'risky_personal': predict_personal_loan({
        'age': 22, 'income': 15000, 'emi': 10000, 'credit_score': 450, 'loan_amount': 5000000, 'tenure': 60
    }),
    'medium_personal': predict_personal_loan({
        'age': 30, 'income': 50000, 'emi': 5000, 'credit_score': 620, 'loan_amount': 1000000, 'tenure': 36
    }),
    'healthy_business': predict_business_loan({
        'annual_revenue': 5000000, 'net_profit': 1000000, 'business_age': 10, 
        'existing_liabilities': 0, 'credit_score': 800, 'loan_amount': 500000, 'tenure': 24
    }),
    'risky_business': predict_business_loan({
        'annual_revenue': 500000, 'net_profit': 50000, 'business_age': 1, 
        'existing_liabilities': 200000, 'credit_score': 500, 'loan_amount': 3000000, 'tenure': 12
    })
}

for name, result in profiles.items():
    print(f"\n=== {name} ===")
    print(json.dumps(result, indent=2))

with open('output_clean.json', 'w') as f:
    json.dump(profiles, f, indent=2)
