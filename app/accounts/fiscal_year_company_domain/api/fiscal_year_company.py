"""HTTP surface for FiscalYearCompany -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.fiscal_year_company_domain.schemas.fiscal_year_company import (

    FiscalYearCompanyListResponse,

    FiscalYearCompanyRead,

)

from app.accounts.fiscal_year_company_domain.services.fiscal_year_company_service import FiscalYearCompanyService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = FiscalYearCompanyService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=FiscalYearCompanyListResponse, summary="List fiscal year company rows")

def list_fiscal_year_companys(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> FiscalYearCompanyListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return FiscalYearCompanyListResponse.from_result(

        page, [FiscalYearCompanyRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=FiscalYearCompanyRead, summary="Get one fiscal year company row"

)

def get_fiscal_year_company(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> FiscalYearCompanyRead:

    try:

        return FiscalYearCompanyRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
