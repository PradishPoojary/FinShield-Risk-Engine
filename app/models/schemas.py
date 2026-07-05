from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TransactionRequest(BaseModel):
    """
    Schema for an incoming transaction from the core banking system or payment gateway.
    """
    transaction_id: str = Field(..., description="Unique UUID for the transaction")
    account_id: str = Field(..., description="Customer Account ID")
    amount: float = Field(..., gt=0, description="Transaction amount (Must be greater than 0)")
    merchant_category: str = Field(..., description="Merchant Category Code (e.g., Retail, Travel, Crypto)")
    device_id: str = Field(..., description="Hardware fingerprint ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RiskAssessmentResponse(BaseModel):
    """
    Schema for the response our engine sends back to the banking gateway.
    """
    transaction_id: str
    status: str = Field(..., description="APPROVED, REVIEW, or BLOCKED")
    risk_score: float = Field(..., description="Probability of fraud (0.0 to 1.0)")
    reason: Optional[str] = Field(default=None, description="Explanation for block/review")