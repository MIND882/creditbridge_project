"""Read-only HTTP surface for Payment Schedule."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.payment_schedule_domain.schemas.payment_schedule import (

    PaymentScheduleListResponse,

    PaymentScheduleRead,

)

from app.accounts.payment_schedule_domain.services.payment_schedule_service import (

    PaymentScheduleService,

)

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentScheduleService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PaymentScheduleListResponse, summary="List payment schedule rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    payment_term_id: Optional[uuid.UUID] = Query(default=None),

    from_date: Optional[date] = Query(default=None),

    to_date: Optional[date] = Query(default=None),

) -> PaymentScheduleListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        payment_term_id=payment_term_id,

        from_date=from_date,

        to_date=to_date,

    )

    return PaymentScheduleListResponse.from_result(

        page, [PaymentScheduleRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PaymentScheduleRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> PaymentScheduleRead:

    try:

        return PaymentScheduleRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
