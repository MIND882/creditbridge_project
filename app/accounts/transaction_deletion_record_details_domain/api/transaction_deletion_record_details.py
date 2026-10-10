"""HTTP surface for Transaction Deletion Record Details -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.transaction_deletion_record_details_domain.schemas.transaction_deletion_record_details import (

    TransactionDeletionRecordDetailsListResponse,

    TransactionDeletionRecordDetailsRead,

)

from app.accounts.transaction_deletion_record_details_domain.services.transaction_deletion_record_details_service import TransactionDeletionRecordDetailsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TransactionDeletionRecordDetailsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=TransactionDeletionRecordDetailsListResponse, summary="List transaction deletion record details rows")

def list_transaction_deletion_record_details(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> TransactionDeletionRecordDetailsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return TransactionDeletionRecordDetailsListResponse.from_result(

        page, [TransactionDeletionRecordDetailsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=TransactionDeletionRecordDetailsRead, summary="Get one transaction deletion record details row")

def get_transaction_deletion_record_details(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> TransactionDeletionRecordDetailsRead:

    try:

        return TransactionDeletionRecordDetailsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
