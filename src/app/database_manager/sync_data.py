# app/database_manager/sync_data.py
from schemas.source_schema import SheetDataCreate
from database_manager.models.models import SheetData
from sqlalchemy.orm import Session

def sync_data_to_db(data: list[SheetDataCreate], db: Session):
    """
    Function to sync fetched sheet data to PostgreSQL.
    """
    for item in data:
        db_sheet_data = SheetData(
            campaign_name=item.campaign_name,
            channel=item.channel,
            impressions=item.impressions,
            ctr_percent=item.ctr_percent,
            conversions=item.conversions,
            cpa_dollars=item.cpa_dollars,
        )
        db.add(db_sheet_data)
    db.commit()
    db.refresh(db_sheet_data)
    return {"message": "Data synced to database successfully!"}
