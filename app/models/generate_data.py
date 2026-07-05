import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta

def generate_banking_data(num_records=2000):
    np.random.seed(42)
    random.seed(42)
    
    merchants = ["Retail", "Gas_Station", "Groceries", "Online_Marketplace", "Travel", "Crypto", "Luxury_Retail"]
    data = []
    start_time = datetime.now() - timedelta(days=30)
    
    for i in range(num_records):
        # Force exactly 10% of the dataset to be fraudulent so the AI can learn the pattern
        is_fraud = 1 if i < (num_records * 0.10) else 0
        
        if is_fraud == 1:
            # Generate obvious fraud patterns (high amounts, crypto/luxury, late night)
            amount = random.uniform(850.0, 4500.0)
            merchant = random.choice(["Crypto", "Luxury_Retail"])
            hour = random.randint(1, 4)
        else:
            # Generate normal legitimate patterns
            amount = round(abs(np.random.normal(50, 100)), 2)
            if amount == 0: amount = 5.0
            merchant = random.choice(merchants)
            hour = random.randint(5, 23)
            
        timestamp = start_time + timedelta(hours=random.randint(0, 720), minutes=random.randint(0, 59))
        timestamp = timestamp.replace(hour=hour)
        
        data.append({
            "transaction_id": str(uuid.uuid4())[:8],
            "account_id": f"ACC-{random.randint(1000, 1100)}",
            "amount": round(amount, 2),
            "merchant_category": merchant,
            "hour_of_day": hour,
            "is_fraud": is_fraud
        })
        
    df = pd.DataFrame(data)
    output_path = "app/models/synthetic_transactions.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Successfully generated {num_records} transaction records.")
    print(f"📊 Fraud distribution: {df['is_fraud'].value_counts().to_dict()}")

if __name__ == "__main__":
    generate_banking_data()