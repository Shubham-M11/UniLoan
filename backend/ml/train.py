import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import os

# Set paths
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/loan_data.csv')
MODEL_PATH = os.path.dirname(__file__)

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # Target variable
    target = 'loan_status'
    X = df.drop(columns=[target])
    y = df[target]

    # Preprocessing
    # Define categorical and numerical features based on dataset
    categorical_cols = ['person_gender', 'person_education', 'person_home_ownership', 'loan_intent', 'previous_loan_defaults_on_file']
    numerical_cols = ['person_age', 'person_income', 'person_emp_exp', 'loan_amnt', 'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length', 'credit_score']

    # Imputers and Scalers
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, numerical_cols),
            ('cat', cat_transformer, categorical_cols)
        ])

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize models
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
        "XGBoost": XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    }

    best_model_name = None
    best_f1 = 0
    best_pipeline = None

    print("Training models...")
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        if hasattr(pipeline, "predict_proba"):
            y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
        else:
            y_pred_proba = [0] * len(y_test) # Fallback

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        print(f"\n--- {name} ---")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"ROC-AUC:   {roc_auc:.4f}")

        # Keep track of the best model based on F1 Score
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline

    print(f"\nBest Model: {best_model_name} with F1 Score: {best_f1:.4f}")
    
    # Save the best pipeline and training data summary for SHAP
    model_file = os.path.join(MODEL_PATH, 'loan_model_pipeline.pkl')
    joblib.dump(best_pipeline, model_file)
    print(f"Saved the best pipeline to {model_file}")
    
    # Save the exact expected training columns for the ML Service to recreate DataFrames properly
    columns_file = os.path.join(MODEL_PATH, 'training_columns.pkl')
    joblib.dump(list(X.columns), columns_file)
    print("Saved categorical encoders/schemas.")

    print("Machine Learning pipeline execution complete.")

if __name__ == "__main__":
    main()
