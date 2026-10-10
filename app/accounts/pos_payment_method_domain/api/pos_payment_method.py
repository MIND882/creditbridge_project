"""HTTP surface for POS Payment Method -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.pos_payment_method_domain.schemas.pos_payment_method import (

    POSPaymentMethodListResponse,

    POSPaymentMethodRead,

)

from app.accounts.pos_payment_method_domain.services.pos_payment_method_service import POSPaymentMethodService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = POSPaymentMethodService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=POSPaymentMethodListResponse, summary="List pos payment method rows")

def list_pos_payment_method(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> POSPaymentMethodListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return POSPaymentMethodListResponse.from_result(

        page, [POSPaymentMethodRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=POSPaymentMethodRead, summary="Get one pos payment method row")

def get_pos_payment_method(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> POSPaymentMethodRead:

    try:

        return POSPaymentMethodRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
