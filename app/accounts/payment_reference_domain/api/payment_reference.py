"""HTTP surface for Payment Reference -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.payment_reference_domain.schemas.payment_reference import (

    PaymentReferenceListResponse,

    PaymentReferenceRead,

)

from app.accounts.payment_reference_domain.services.payment_reference_service import PaymentReferenceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentReferenceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PaymentReferenceListResponse, summary="List payment reference rows")

def list_payment_reference(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PaymentReferenceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PaymentReferenceListResponse.from_result(

        page, [PaymentReferenceRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PaymentReferenceRead, summary="Get one payment reference row")

def get_payment_reference(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PaymentReferenceRead:

    try:

        return PaymentReferenceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
