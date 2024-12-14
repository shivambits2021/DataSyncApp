from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, TIMESTAMP
from datetime import datetime

Base = declarative_base()

class SheetData(Base):
    __tablename__ = 'sheet_data'  # This will be the name of the table in PostgreSQL

    # Define the columns for the table
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    campaign_name = Column(String, index=True)  # Campaign Name
    channel = Column(String)  # Channel
    impressions = Column(Integer)  # Impressions
    ctr_percent = Column(Float)  # CTR (%)
    conversions = Column(Integer)  # Conversions
    cpa_dollars = Column(Float)  # CPA ($)

    def __repr__(self):
        return f"<SheetData(campaign_name={self.campaign_name}, channel={self.channel})>"
    


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    sheet_id = Column(String(255), nullable=True)
    token_expiry = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
