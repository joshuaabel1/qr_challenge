# app/api/routers/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies.db import get_db
from app.api.schemas.auth_schemas import UserRegisterRequest, UserRegisterResponse, TokenResponse
from app.services.auth_service import register_user, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRegisterResponse)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, request.email, request.password)
    return UserRegisterResponse(email=user.email)

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: UserRegisterRequest = Depends(),
    db: Session = Depends(get_db)
):
    token = authenticate_user(db, form_data.username, form_data.password)
    return TokenResponse(access_token=token)
