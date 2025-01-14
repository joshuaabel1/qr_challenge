# main.py
from fastapi import FastAPI
from app.api.routers import auth, qr, scan
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

# Crear tablas en la BD (para ambiente de desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Incluir routers
app.include_router(auth.router)
app.include_router(qr.router)
app.include_router(scan.router)
