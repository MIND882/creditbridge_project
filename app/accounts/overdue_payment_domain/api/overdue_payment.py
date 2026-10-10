"""HTTP surface for Overdue Payment -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.overdue_payment_domain.schemas.overdue_payment import (

    OverduePaymentListResponse,

    OverduePaymentRead,

)

from app.accounts.overdue_payment_domain.services.overdue_payment_service import OverduePaymentService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = OverduePaymentService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=OverduePaymentListResponse, summary="List overdue payment rows")

def list_overdue_payment(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> OverduePaymentListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return OverduePaymentListResponse.from_result(

        page, [OverduePaymentRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=OverduePaymentRead, summary="Get one overdue payment row")

def get_overdue_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> OverduePaymentRead:

    try:

        return OverduePaymentRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
