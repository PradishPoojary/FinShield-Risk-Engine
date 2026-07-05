from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# The physical file where our banking audit logs will be permanently saved
SQLALCHEMY_DATABASE_URL = "sqlite:///./finshield_audit.db"

# Create the engine that acts as the bridge between Python and the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory to handle individual database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class that our database tables will inherit from
Base = declarative_base()

class TransactionAudit(Base):
    """
    SQLAlchemy ORM Model representing the 'transaction_audit_logs' table.
    """
    __tablename__ = "transaction_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    account_id = Column(String, index=True)
    amount = Column(Float)
    merchant_category = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # AI Decision Data
    risk_score = Column(Float)
    decision_status = Column(String)  # APPROVED, REVIEW, BLOCKED
    reason = Column(String)