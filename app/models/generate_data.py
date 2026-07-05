import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta

def generate_banking_data(num_records=2000):
    """
    Generates synthetic banking transaction data with realistic fraudulent patterns.
    """
    np.random.seed(42)
    random.seed(42)
    
    merchants = ["Retail", "Gas_Station", "Groceries", "Online_Marketplace", "Travel", "Crypto", "Luxury_Retail"]
    
    data = []
    start_time = datetime.now() - timedelta(days=30)
    
    for _ in range(num_records):
        # Base distributions for regular legitimate activity
        amount = round(abs(np.random.normal(50, 100)), 2)
        if amount == 0: amount = 5.0
            
        merchant = random.choice(merchants)
        # Random hour between 0 and 23
        hour = random.randint(0, 23)
        timestamp = start_time + timedelta(hours=random.randint(0, 720), minutes=random.randint(0, 59))
        timestamp = timestamp.replace(hour=hour)
        
        # Initialize flags
        is_fraud = 0
        
        # Inject Complex Fraud Rules / Scenarios
        # Scenario 1: High amount transaction in high-risk categories (Crypto/Luxury Retail)
        if merchant in ["Crypto", "Luxury_Retail"] and amount > 800:
            if random.random() < 0.7:  # 70% chance this anomaly is fraudulent
                is_fraud = 1
                
        # Scenario 2: High amount transactions occurring during late-night hours (1 AM to 4 AM)
        if hour >= 1 and hour <= 4 and amount > 500:
            if random.random() < 0.8:
                is_fraud = 1
                
        # Scenario 3: Purely random outlier high-velocity anomalies
        if amount > 4500:
            is_fraud = 1

        data.append({
            "transaction_id": str(uuid.uuid4())[:8],
            "account_id": f"ACC-{random.randint(1000, 1100)}",
            "amount": amount,
            "merchant_category": merchant,
            "hour_of_day": hour,
            "is_fraud": is_fraud
        })
        
    df = pd.DataFrame(data)
    
    # Save to the models directory for the training script to consume
    output_path = "app/models/synthetic_transactions.csv"
    df.to_csv(output_path, index=False)
    print(f" Successfully generated {num_records} transaction records at: {output_path}")
    print(f" Fraud distribution: {df['is_fraud'].value_counts().to_dict()}")

if __name__ == "__main__":
    generate_banking_data()