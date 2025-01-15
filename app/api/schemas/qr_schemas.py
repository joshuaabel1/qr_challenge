from pydantic import BaseModel, HttpUrl, UUID4
from pydantic import BaseModel, validator
from typing import Optional

class QRCreateRequest(BaseModel):
    url: HttpUrl
    color: Optional[str] = "black"
    size: Optional[int] = 8

    @validator("color", pre=True)
    def default_color_if_empty(cls, v):
        if not v or v.strip() == "":
            return "black"
        return v
       
    @validator("size", pre=True)
    def default_size_if_empty(cls, v):
        if v is None:
            return 8
        return v


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
        from_attributes = True
