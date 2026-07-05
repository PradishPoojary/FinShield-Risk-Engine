import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_fraud_model():
    print("🔄 Loading synthetic banking data...")
    # Load the generated dataset
    df = pd.read_csv("app/models/synthetic_transactions.csv")
    
    # Preprocessing: Convert categorical text data (Merchant Categories) into numerical indicators
    # This process (One-Hot Encoding) is standard for production grading models
    df_encoded = pd.get_dummies(df, columns=["merchant_category"], drop_first=True)
    
    # Save the feature columns layout so the API knows exactly what order features are in
    feature_columns = [col for col in df_encoded.columns if col not in ["transaction_id", "account_id", "is_fraud"]]
    
    with open("app/models/feature_columns.pkl", "wb") as f:
        pickle.dump(feature_columns, f)
        
    # Define Inputs (X) and Target Label (y)
    X = df_encoded[feature_columns]
    y = df_encoded["is_fraud"]
    
    # Split into 80% training data and 20% validation data to evaluate performance
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"🏋️ Training Random Forest Classifier on {len(X_train)} samples...")
    # Train the ensemble model
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)
    
    # Evaluate performance
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n📊 Model Performance Report:")
    print(f"Overall Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Metrics:")
    print(classification_report(y_test, y_pred))
    
    # Save the trained model to disk
    model_path = "app/models/fraud_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    print(f"✅ Production-ready model saved successfully at: {model_path}")

if __name__ == "__main__":
    train_fraud_model()