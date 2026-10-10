"""HTTP surface for Financial Report Row -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.financial_report_row_domain.schemas.financial_report_row import (

    FinancialReportRowListResponse,

    FinancialReportRowRead,

)

from app.accounts.financial_report_row_domain.services.financial_report_row_service import FinancialReportRowService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = FinancialReportRowService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=FinancialReportRowListResponse, summary="List financial report row rows")

def list_financial_report_row(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> FinancialReportRowListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return FinancialReportRowListResponse.from_result(

        page, [FinancialReportRowRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=FinancialReportRowRead, summary="Get one financial report row row")

def get_financial_report_row(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> FinancialReportRowRead:

    try:

        return FinancialReportRowRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
