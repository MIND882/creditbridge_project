"""HTTP surface for Repost Accounting Ledger Items -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.repost_accounting_ledger_items_domain.schemas.repost_accounting_ledger_items import (

    RepostAccountingLedgerItemsListResponse,

    RepostAccountingLedgerItemsRead,

)

from app.accounts.repost_accounting_ledger_items_domain.services.repost_accounting_ledger_items_service import RepostAccountingLedgerItemsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = RepostAccountingLedgerItemsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=RepostAccountingLedgerItemsListResponse, summary="List repost accounting ledger items rows")

def list_repost_accounting_ledger_items(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> RepostAccountingLedgerItemsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return RepostAccountingLedgerItemsListResponse.from_result(

        page, [RepostAccountingLedgerItemsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=RepostAccountingLedgerItemsRead, summary="Get one repost accounting ledger items row")

def get_repost_accounting_ledger_items(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> RepostAccountingLedgerItemsRead:

    try:

        return RepostAccountingLedgerItemsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
