"""HTTP surface for Supplier Scorecard Scoring Variable -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_variable_domain.schemas.supplier_scorecard_scoring_variable import (

    SupplierScorecardScoringVariableListResponse,

    SupplierScorecardScoringVariableRead,

)

from app.buying.supplier_scorecard_scoring_variable_domain.services.supplier_scorecard_scoring_variable_service import SupplierScorecardScoringVariableService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SupplierScorecardScoringVariableService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SupplierScorecardScoringVariableListResponse, summary="List supplier scorecard scoring variable rows")

def list_supplier_scorecard_scoring_variable(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SupplierScorecardScoringVariableListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SupplierScorecardScoringVariableListResponse.from_result(

        page, [SupplierScorecardScoringVariableRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=SupplierScorecardScoringVariableRead, summary="Get one supplier scorecard scoring variable row"

)

def get_supplier_scorecard_scoring_variable(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SupplierScorecardScoringVariableRead:

    try:

        return SupplierScorecardScoringVariableRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
