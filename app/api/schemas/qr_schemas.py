# app/api/schemas/qr_schemas.py
from pydantic import BaseModel, HttpUrl, UUID4


class QRCreateRequest(BaseModel):
    url: HttpUrl
    color: str
    size: int

class QRUpdateRequest(BaseModel):
    url: HttpUrl | None = None
    color: str | None = None
    size: int | None = None

class QRResponse(BaseModel):
    uuid: UUID4
    url: str
    color: str
    size: int

    class Config:
        # Permite a Pydantic leer directamente objetos de SQLAlchemy
        from_attributes = True
