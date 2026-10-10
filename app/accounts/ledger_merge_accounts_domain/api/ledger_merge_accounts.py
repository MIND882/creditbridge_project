"""HTTP surface for Ledger Merge Accounts -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.ledger_merge_accounts_domain.schemas.ledger_merge_accounts import (

    LedgerMergeAccountsListResponse,

    LedgerMergeAccountsRead,

)

from app.accounts.ledger_merge_accounts_domain.services.ledger_merge_accounts_service import LedgerMergeAccountsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LedgerMergeAccountsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=LedgerMergeAccountsListResponse, summary="List ledger merge accounts rows")

def list_ledger_merge_accounts(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> LedgerMergeAccountsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return LedgerMergeAccountsListResponse.from_result(

        page, [LedgerMergeAccountsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=LedgerMergeAccountsRead, summary="Get one ledger merge accounts row")

def get_ledger_merge_accounts(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LedgerMergeAccountsRead:

    try:

        return LedgerMergeAccountsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
