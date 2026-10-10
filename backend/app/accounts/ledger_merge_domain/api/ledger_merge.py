"""HTTP surface for Ledger Merge."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.ledger_merge_domain.schemas.ledger_merge import (

        LedgerMergeCreate,

    LedgerMergeUpdate,

    LedgerMergeRead,

    LedgerMergeListResponse,

)

from app.accounts.ledger_merge_domain.services.ledger_merge_service import LedgerMergeService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LedgerMergeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=LedgerMergeRead, status_code=status.HTTP_201_CREATED,

    summary="Create a ledger merge",

)

def create_ledger_merge(

    payload: LedgerMergeCreate, db: DbDep, business_id: BusinessDep

) -> LedgerMergeRead:

    try:

        return LedgerMergeRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=LedgerMergeListResponse, summary="List ledger merges")

def list_ledger_merge(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> LedgerMergeListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

    )

    return LedgerMergeListResponse.from_result(

        page, [LedgerMergeRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=LedgerMergeRead, summary="Get one ledger merge"

)

def get_ledger_merge(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LedgerMergeRead:

    try:

        return LedgerMergeRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=LedgerMergeRead, summary="Update")

def update_ledger_merge(

    row_id: uuid.UUID, payload: LedgerMergeUpdate, db: DbDep, business_id: BusinessDep

) -> LedgerMergeRead:

    try:

        return LedgerMergeRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_ledger_merge(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to NoneType and then rejects for a

    # 204 at import time.

    try:

        _service.delete(db, business_id, row_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
