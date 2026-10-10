"""

HTTP surface for Accounting Dimension Detail.



Read-only by design: this is a Frappe child table (``istable: 1``), so rows are

created and edited through the parent Accounting Dimension endpoints. Exposing writes here

would let a client bypass the parent service's invariants.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.accounting_dimension_detail_domain.schemas.accounting_dimension_detail import AccountingDimensionDetailListResponse, AccountingDimensionDetailRead

from app.accounts.accounting_dimension_detail_domain.services.accounting_dimension_detail_service import AccountingDimensionDetailService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()

_service = AccountingDimensionDetailService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> AccountingDimensionDetailRead:

    return AccountingDimensionDetailRead.model_validate(row)





@router.get("", response_model=AccountingDimensionDetailListResponse, summary="List rows")

def list_rows(

    db: DbDep, business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> AccountingDimensionDetailListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return AccountingDimensionDetailListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/{row_id}", response_model=AccountingDimensionDetailRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> AccountingDimensionDetailRead:

    try:

        return _read(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
