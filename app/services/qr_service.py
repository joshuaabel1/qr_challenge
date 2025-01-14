import qrcode
import io
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.db.models import QRCode

def create_qr(db: Session, user_uuid: uuid.UUID, url: str, color: str, size: int) -> QRCode:
    qr_code = QRCode(
        url=url,
        color=color,
        size=size,
        user_uuid=user_uuid
    )
    db.add(qr_code)
    db.commit()
    db.refresh(qr_code)
    return qr_code

def generate_qr_image(url: str, color: str, size: int) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        box_size=size,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def update_qr(db: Session, qr_uuid: uuid.UUID, **kwargs) -> QRCode:
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR code no encontrado"
        )
    for key, value in kwargs.items():
        if value is not None:
            setattr(qr_code, key, value)
    qr_code.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(qr_code)
    return qr_code

def get_user_qrs(db: Session, user_uuid: uuid.UUID) -> list[QRCode]:
    return db.query(QRCode).filter(QRCode.user_uuid == user_uuid).all()
