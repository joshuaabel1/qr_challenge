from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.dependencies.db import get_db, get_current_active_user
from app.api.schemas.scan_schemas import ScanResponse
from app.services.scan_service import register_scan, get_scans_by_qr
from app.db.models import QRCode

router = APIRouter(prefix="/scan", tags=["Scans"])

@router.get("/{qr_uuid}")
def simulate_scan(
    qr_uuid: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user= Depends(get_current_active_user),
):
    """
    Simula el escaneo de un QR.
    Registra IP/país/timestamp y redirige a la URL.
    """
    client_ip = request.client.host

    scan = register_scan(db, qr_uuid, client_ip)

    qr_code = db.query(QRCode).filter(
        QRCode.uuid == qr_uuid
    ).first()
    if not qr_code:
        return Response(
            content="QR not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return Response(
        status_code=status.HTTP_302_FOUND,
        headers={"Location": qr_code.url}
    )

@router.get("/stats/{qr_uuid}", response_model=dict)
def get_qr_stats(
    qr_uuid: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Retorna estadísticas de escaneos de un QR en particular.
    """
    scans = get_scans_by_qr(db, qr_uuid)
    total_scans = len(scans)

    scans_data = []
    for scan in scans:
        scans_data.append(ScanResponse(
            uuid=str(scan.uuid),
            ip=scan.ip,
            country=scan.country,
            timestamp=scan.timestamp.isoformat(),
        ))

    return {
        "total_scans": total_scans,
        "scans_detail": scans_data
    }
