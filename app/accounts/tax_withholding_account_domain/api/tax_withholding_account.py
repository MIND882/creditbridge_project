"""Read-only HTTP surface for TaxWithholdingAccount."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_account_domain.schemas.tax_withholding_account import TaxWithholdingAccountListResponse, TaxWithholdingAccountRead

from app.accounts.tax_withholding_account_domain.services.tax_withholding_account_service import TaxWithholdingAccountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TaxWithholdingAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=TaxWithholdingAccountListResponse, summary="List TaxWithholdingAccount rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> TaxWithholdingAccountListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return TaxWithholdingAccountListResponse.from_result(

        page, [TaxWithholdingAccountRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=TaxWithholdingAccountRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> TaxWithholdingAccountRead:

    try:

        return TaxWithholdingAccountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
