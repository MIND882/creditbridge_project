"""HTTP surface for Unreconcile Payment Entries -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.unreconcile_payment_entries_domain.schemas.unreconcile_payment_entries import (

    UnreconcilePaymentEntriesListResponse,

    UnreconcilePaymentEntriesRead,

)

from app.accounts.unreconcile_payment_entries_domain.services.unreconcile_payment_entries_service import UnreconcilePaymentEntriesService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = UnreconcilePaymentEntriesService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=UnreconcilePaymentEntriesListResponse, summary="List unreconcile payment entries rows")

def list_unreconcile_payment_entries(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> UnreconcilePaymentEntriesListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return UnreconcilePaymentEntriesListResponse.from_result(

        page, [UnreconcilePaymentEntriesRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=UnreconcilePaymentEntriesRead, summary="Get one unreconcile payment entries row")

def get_unreconcile_payment_entries(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> UnreconcilePaymentEntriesRead:

    try:

        return UnreconcilePaymentEntriesRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
