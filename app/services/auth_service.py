# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from fastapi import HTTPException, status
from jose import jwt, JWTError

def register_user(db: Session, email: str, password: str) -> User:
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )

    hashed_password = get_password_hash(password)
    new_user = User(email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email_or_user: str, password: str) -> str:
    user = db.query(User).filter(User.email == email_or_user).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return create_access_token({"sub": str(user.uuid)})

def get_current_user(db: Session, token: str) -> User:
    """
    Decodificar token y obtener usuario para la dependencia de seguridad.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.uuid == user_id).first()
    if user is None:
        raise credentials_exception
    return user
