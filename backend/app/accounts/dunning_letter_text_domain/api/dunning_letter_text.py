"""Read-only HTTP surface for DunningLetterText."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.dunning_letter_text_domain.schemas.dunning_letter_text import DunningLetterTextListResponse, DunningLetterTextRead

from app.accounts.dunning_letter_text_domain.services.dunning_letter_text_service import DunningLetterTextService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = DunningLetterTextService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=DunningLetterTextListResponse, summary="List DunningLetterText rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> DunningLetterTextListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return DunningLetterTextListResponse.from_result(

        page, [DunningLetterTextRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=DunningLetterTextRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> DunningLetterTextRead:

    try:

        return DunningLetterTextRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
