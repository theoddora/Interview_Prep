from pydantic import BaseModel
from datetime import datetime

class StatsSchema(BaseModel):
    total_emails: int
    forwarded_emails: int
    responded_emails: int
    timestamp: datetime

    class Config:
        orm_mode = True