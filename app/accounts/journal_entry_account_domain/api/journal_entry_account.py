"""Read-only HTTP surface for JournalEntryAccount."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.journal_entry_account_domain.schemas.journal_entry_account import JournalEntryAccountListResponse, JournalEntryAccountRead

from app.accounts.journal_entry_account_domain.services.journal_entry_account_service import JournalEntryAccountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = JournalEntryAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=JournalEntryAccountListResponse, summary="List journal entry account rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> JournalEntryAccountListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return JournalEntryAccountListResponse.from_result(page, [JournalEntryAccountRead.model_validate(r) for r in page.items])





@router.get("/{row_id}", response_model=JournalEntryAccountRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> JournalEntryAccountRead:

    try:

        return JournalEntryAccountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
