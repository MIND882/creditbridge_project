"""HTTP surface for Cashier Closing Payments -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.cashier_closing_payments_domain.schemas.cashier_closing_payments import (

    CashierClosingPaymentsListResponse,

    CashierClosingPaymentsRead,

)

from app.accounts.cashier_closing_payments_domain.services.cashier_closing_payments_service import CashierClosingPaymentsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = CashierClosingPaymentsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=CashierClosingPaymentsListResponse, summary="List cashier closing payments rows")

def list_cashier_closing_payments(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> CashierClosingPaymentsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return CashierClosingPaymentsListResponse.from_result(

        page, [CashierClosingPaymentsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=CashierClosingPaymentsRead, summary="Get one cashier closing payments row")

def get_cashier_closing_payments(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CashierClosingPaymentsRead:

    try:

        return CashierClosingPaymentsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
