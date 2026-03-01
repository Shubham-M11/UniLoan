import json
from services.ml_service import predict_personal_loan

def main():
    healthy_profile = {
        'age': 35, 
        'income': 200000, 
        'emi': 0, 
        'credit_score': 800, 
        'loan_amount': 100000, 
        'tenure': 12
    }
    
    risky_profile = {
        'age': 25, 
        'income': 20000, 
        'emi': 10000, 
        'credit_score': 500, 
        'loan_amount': 2000000, 
        'tenure': 60
    }
    
    print("=== HEALTHY PROFILE ===")
    print(json.dumps(predict_personal_loan(healthy_profile), indent=2))
    print("\n=== RISKY PROFILE ===")
    print(json.dumps(predict_personal_loan(risky_profile), indent=2))

if __name__ == "__main__":
    main()
