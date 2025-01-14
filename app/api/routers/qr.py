# app/api/routers/qr.py
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.models import QRCode
from app.api.dependencies.db import get_db, get_current_active_user
from app.api.schemas.qr_schemas import QRCreateRequest, QRUpdateRequest, QRResponse
from app.services.qr_service import create_qr, generate_qr_image, update_qr, get_user_qrs

router = APIRouter(prefix="/qr", tags=["QR Codes"])

@router.post("/generate")
def generate_qr_code(
    request: QRCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Endpoint para generar un código QR y retornarlo como archivo PNG descargable.
    - request (QRCreateRequest): { url, color, size }
    """
    qr_code = create_qr(
        db=db,
        user_uuid=current_user.uuid,
        url=str(request.url),
        color=request.color,
        size=request.size
    )
    
    img_bytes = generate_qr_image(qr_code.url, qr_code.color, qr_code.size)

    return Response(
        content=img_bytes,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=qr.png"}
    )


@router.patch("/update/{qr_uuid}", response_model=QRResponse)
def update_qr_code(
    qr_uuid: str,
    request: QRUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Actualiza propiedades de un QR existente: color, tamaño o URL.
    Retorna el QR en JSON con los cambios aplicados.
    """
    db_qr = db.query(QRCode).filter(
        QRCode.uuid == qr_uuid,
        QRCode.user_uuid == current_user.uuid
    ).first()

    if not db_qr:
        return Response(
            content="QR not found or not owned by user",
            status_code=status.HTTP_404_NOT_FOUND
        )

    updated_qr = update_qr(db, db_qr.uuid, **request.dict(exclude_unset=True))
    return updated_qr


@router.get("/list", response_model=list[QRResponse])
def list_user_qr_codes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Retorna todos los QR generados por el usuario actual.
    """
    qrs = get_user_qrs(db, current_user.uuid)
    return qrs

@router.get("/{qr_uuid}")
def get_qr_image(
    qr_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Dado un UUID, devuelve la imagen PNG del QR correspondiente,
    si le pertenece al usuario.
    """
    db_qr = db.query(QRCode).filter(
        QRCode.uuid == qr_uuid,
        QRCode.user_uuid == current_user.uuid
    ).first()
    if not db_qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR not found or not owned by user"
        )

    # Generar la imagen en memoria
    img_bytes = generate_qr_image(db_qr.url, db_qr.color, db_qr.size)
    
    # Retornar como archivo PNG
    return Response(
        content=img_bytes,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=qr.png"}
    )