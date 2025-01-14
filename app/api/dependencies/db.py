# app/api/dependencies/db.py
from typing import Generator
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.services.auth_service import get_current_user
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_active_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return get_current_user(db, token)