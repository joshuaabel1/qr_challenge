from pydantic import BaseModel, UUID4
from datetime import datetime

class ScanResponse(BaseModel):
    uuid: UUID4
    ip: str
    country: str | None = None
    timestamp: datetime

    model_config = {"from_attributes": True}
