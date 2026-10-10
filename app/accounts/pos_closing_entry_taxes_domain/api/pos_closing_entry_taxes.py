"""HTTP surface for POS Closing Entry Taxes -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.pos_closing_entry_taxes_domain.schemas.pos_closing_entry_taxes import (

    POSClosingEntryTaxesListResponse,

    POSClosingEntryTaxesRead,

)

from app.accounts.pos_closing_entry_taxes_domain.services.pos_closing_entry_taxes_service import POSClosingEntryTaxesService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = POSClosingEntryTaxesService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=POSClosingEntryTaxesListResponse, summary="List pos closing entry taxes rows")

def list_pos_closing_entry_taxes(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> POSClosingEntryTaxesListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return POSClosingEntryTaxesListResponse.from_result(

        page, [POSClosingEntryTaxesRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=POSClosingEntryTaxesRead, summary="Get one pos closing entry taxes row")

def get_pos_closing_entry_taxes(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> POSClosingEntryTaxesRead:

    try:

        return POSClosingEntryTaxesRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
