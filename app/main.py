from fastapi import FastAPI, HTTPException, Depends
import pickle
import pandas as pd
from sqlalchemy.orm import Session
from app.models.schemas import TransactionRequest, RiskAssessmentResponse
from app.database import SessionLocal, engine, Base, TransactionAudit

# 1. Initialize the Database Tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinShield Enterprise Risk Engine",
    description="Asynchronous AI-driven banking transaction fraud detection middle-layer with immutable audit logging.",
    version="1.1.0"
)

MODEL_PATH = "app/models/fraud_model.pkl"
FEATURES_PATH = "app/models/feature_columns.pkl"

model = None
feature_columns = None

@app.on_event("startup")
def load_assets():
    global model, feature_columns
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(FEATURES_PATH, "rb") as f:
            feature_columns = pickle.load(f)
        print("🚀 AI Models, Feature Layouts, and Database Engine loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: Model files not found.")
        raise RuntimeError("Model files missing.")

# Dependency to get a database session per API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "HEALTHY", "service": "FinShield-Risk-Engine", "database": "CONNECTED"}

@app.post("/api/v1/transactions/verify", response_model=RiskAssessmentResponse)
async def verify_transaction(transaction: TransactionRequest, db: Session = Depends(get_db)):
    if model is None or feature_columns is None:
        raise HTTPException(status_code=503, detail="Risk Engine uninitialized.")

    try:
        # AI Inference Data Prep
        input_data = {
            "amount": transaction.amount,
            "hour_of_day": transaction.timestamp.hour
        }
        
        for col in feature_columns:
            if col.startswith("merchant_category_"):
                input_data[col] = 0
                
        target_merchant_col = f"merchant_category_{transaction.merchant_category}"
        if target_merchant_col in input_data:
            input_data[target_merchant_col] = 1
            
        input_df = pd.DataFrame([input_data])[feature_columns]
        
        # AI Prediction
        prediction = int(model.predict(input_df)[0])
        probabilities = model.predict_proba(input_df)[0]
        risk_score = float(probabilities[1])

        # Business Logic
        if prediction == 1:
            status = "BLOCKED"
            reason = f"High risk transaction flagged by AI Engine (Risk Score: {risk_score:.2f})."
        elif risk_score > 0.35:
            status = "REVIEW"
            reason = "Moderate anomaly variance detected. Route to fraud operations team."
        else:
            status = "APPROVED"
            reason = "Transaction clearing threshold satisfied."

        # IMMUTABLE DATABASE AUDIT LOG INJECTION
        audit_record = TransactionAudit(
            transaction_id=transaction.transaction_id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            merchant_category=transaction.merchant_category,
            timestamp=transaction.timestamp.replace(tzinfo=None), # SQLite requires naive datetimes
            risk_score=risk_score,
            decision_status=status,
            reason=reason
        )
        db.add(audit_record)
        db.commit()

        # API Response
        return RiskAssessmentResponse(
            transaction_id=transaction.transaction_id,
            status=status,
            risk_score=risk_score,
            reason=reason
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")