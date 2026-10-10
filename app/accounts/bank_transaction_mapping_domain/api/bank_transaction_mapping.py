"""

HTTP surface for Bank Transaction Mapping.



Read-only by design: this is a Frappe child table (``istable: 1``), so rows are

created and edited through the parent Bank endpoints. Exposing writes here

would let a client bypass the parent service's invariants.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_mapping_domain.schemas.bank_transaction_mapping import BankTransactionMappingListResponse, BankTransactionMappingRead

from app.accounts.bank_transaction_mapping_domain.services.bank_transaction_mapping_service import BankTransactionMappingService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()

_service = BankTransactionMappingService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankTransactionMappingRead:

    return BankTransactionMappingRead.model_validate(row)





@router.get("", response_model=BankTransactionMappingListResponse, summary="List rows")

def list_rows(

    db: DbDep, business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> BankTransactionMappingListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return BankTransactionMappingListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/{row_id}", response_model=BankTransactionMappingRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> BankTransactionMappingRead:

    try:

        return _read(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
