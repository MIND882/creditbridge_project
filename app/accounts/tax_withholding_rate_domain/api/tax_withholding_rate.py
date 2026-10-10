"""Read-only HTTP surface for TaxWithholdingRate."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_rate_domain.schemas.tax_withholding_rate import TaxWithholdingRateListResponse, TaxWithholdingRateRead

from app.accounts.tax_withholding_rate_domain.services.tax_withholding_rate_service import TaxWithholdingRateService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TaxWithholdingRateService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=TaxWithholdingRateListResponse, summary="List TaxWithholdingRate rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> TaxWithholdingRateListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return TaxWithholdingRateListResponse.from_result(

        page, [TaxWithholdingRateRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=TaxWithholdingRateRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> TaxWithholdingRateRead:

    try:

        return TaxWithholdingRateRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
