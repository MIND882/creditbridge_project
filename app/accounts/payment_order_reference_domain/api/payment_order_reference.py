"""HTTP surface for Payment Order Reference -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.payment_order_reference_domain.schemas.payment_order_reference import (

    PaymentOrderReferenceListResponse,

    PaymentOrderReferenceRead,

)

from app.accounts.payment_order_reference_domain.services.payment_order_reference_service import PaymentOrderReferenceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentOrderReferenceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PaymentOrderReferenceListResponse, summary="List payment order reference rows")

def list_payment_order_reference(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PaymentOrderReferenceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PaymentOrderReferenceListResponse.from_result(

        page, [PaymentOrderReferenceRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PaymentOrderReferenceRead, summary="Get one payment order reference row")

def get_payment_order_reference(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PaymentOrderReferenceRead:

    try:

        return PaymentOrderReferenceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
