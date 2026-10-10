"""HTTP surface for Subscription Invoice -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.subscription_invoice_domain.schemas.subscription_invoice import (

    SubscriptionInvoiceListResponse,

    SubscriptionInvoiceRead,

)

from app.accounts.subscription_invoice_domain.services.subscription_invoice_service import SubscriptionInvoiceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SubscriptionInvoiceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SubscriptionInvoiceListResponse, summary="List subscription invoice rows")

def list_subscription_invoice(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SubscriptionInvoiceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SubscriptionInvoiceListResponse.from_result(

        page, [SubscriptionInvoiceRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=SubscriptionInvoiceRead, summary="Get one subscription invoice row")

def get_subscription_invoice(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SubscriptionInvoiceRead:

    try:

        return SubscriptionInvoiceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
