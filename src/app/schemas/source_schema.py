# app\schemas\source_schema.py
from pydantic import BaseModel

class SheetDataBase(BaseModel):
    campaign_name: str
    channel: str
    impressions: int
    ctr_percent: float
    conversions: int
    cpa_dollars: float

class SheetDataCreate(SheetDataBase):
    pass
