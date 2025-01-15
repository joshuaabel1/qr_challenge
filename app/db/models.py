import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QRCode(Base):
    __tablename__ = "qr_codes"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False)
    color = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))

class Scan(Base):
    __tablename__ = "scans"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    qr_uuid = Column(UUID(as_uuid=True), ForeignKey("qr_codes.uuid"))
    ip = Column(String, nullable=False)
    country = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
