from sqlalchemy.orm import Session
from app.db.models import Scan, QRCode
from fastapi import HTTPException, status
import uuid
import requests

def register_scan(db: Session, qr_uuid: uuid.UUID, ip: str) -> Scan:
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR code no encontrado"
        )

    country = get_country_from_ip(ip)

    new_scan = Scan(qr_uuid=qr_code.uuid, ip=ip, country=country)
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    return new_scan

def get_country_from_ip(ip: str) -> str | None:
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        if response.status_code == 200:
            data = response.json()
            print(data)
            return data.get("country_name")
    except:
        pass
    return None

def get_scans_by_qr(db: Session, qr_uuid: uuid.UUID) -> list[Scan]:
    return db.query(Scan).filter(Scan.qr_uuid == qr_uuid).all()
