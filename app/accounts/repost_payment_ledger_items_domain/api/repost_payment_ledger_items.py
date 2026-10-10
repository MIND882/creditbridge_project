"""HTTP surface for Repost Payment Ledger Items -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.repost_payment_ledger_items_domain.schemas.repost_payment_ledger_items import (

    RepostPaymentLedgerItemsListResponse,

    RepostPaymentLedgerItemsRead,

)

from app.accounts.repost_payment_ledger_items_domain.services.repost_payment_ledger_items_service import RepostPaymentLedgerItemsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = RepostPaymentLedgerItemsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=RepostPaymentLedgerItemsListResponse, summary="List repost payment ledger items rows")

def list_repost_payment_ledger_items(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> RepostPaymentLedgerItemsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return RepostPaymentLedgerItemsListResponse.from_result(

        page, [RepostPaymentLedgerItemsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=RepostPaymentLedgerItemsRead, summary="Get one repost payment ledger items row")

def get_repost_payment_ledger_items(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> RepostPaymentLedgerItemsRead:

    try:

        return RepostPaymentLedgerItemsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
