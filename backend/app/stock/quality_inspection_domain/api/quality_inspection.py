"""HTTP surface for Quality Inspection."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.stock.quality_inspection_domain.schemas.quality_inspection import (

    QualityInspectionCreate,

    QualityInspectionUpdate,

    QualityInspectionRead,

    QualityInspectionListResponse,

)

from app.stock.quality_inspection_domain.services.quality_inspection_service import QualityInspectionService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = QualityInspectionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=QualityInspectionRead, status_code=status.HTTP_201_CREATED,

    summary="Create a quality inspection",

)

def create_quality_inspection(

    payload: QualityInspectionCreate, db: DbDep, business_id: BusinessDep

) -> QualityInspectionRead:

    try:

        return QualityInspectionRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=QualityInspectionListResponse, summary="List quality inspections")

def list_quality_inspection(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> QualityInspectionListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return QualityInspectionListResponse.from_result(

        page, [QualityInspectionRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=QualityInspectionRead, summary="Get one quality inspection"

)

def get_quality_inspection(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> QualityInspectionRead:

    try:

        return QualityInspectionRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=QualityInspectionRead, summary="Update")

def update_quality_inspection(

    row_id: uuid.UUID, payload: QualityInspectionUpdate, db: DbDep, business_id: BusinessDep

) -> QualityInspectionRead:

    try:

        return QualityInspectionRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_quality_inspection(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to NoneType and then rejects for a

    # 204 at import time.

    try:

        _service.delete(db, business_id, row_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post("/{row_id}/submit", response_model=QualityInspectionRead, summary="Submit")

def submit_quality_inspection(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> QualityInspectionRead:

    try:

        return QualityInspectionRead.model_validate(_service.submit(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=QualityInspectionRead, summary="Cancel")

def cancel_quality_inspection(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> QualityInspectionRead:

    try:

        return QualityInspectionRead.model_validate(_service.cancel(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
