"""HTTP surface for Supplier Scorecard Period."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_period_domain.schemas.supplier_scorecard_period import (

    SupplierScorecardPeriodCreate,

    SupplierScorecardPeriodUpdate,

    SupplierScorecardPeriodRead,

    SupplierScorecardPeriodListResponse,

)

from app.buying.supplier_scorecard_period_domain.services.supplier_scorecard_period_service import SupplierScorecardPeriodService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SupplierScorecardPeriodService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=SupplierScorecardPeriodRead, status_code=status.HTTP_201_CREATED,

    summary="Create a supplier scorecard period",

)

def create_supplier_scorecard_period(

    payload: SupplierScorecardPeriodCreate, db: DbDep, business_id: BusinessDep

) -> SupplierScorecardPeriodRead:

    try:

        return SupplierScorecardPeriodRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=SupplierScorecardPeriodListResponse, summary="List supplier scorecard periods")

def list_supplier_scorecard_period(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> SupplierScorecardPeriodListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return SupplierScorecardPeriodListResponse.from_result(

        page, [SupplierScorecardPeriodRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=SupplierScorecardPeriodRead, summary="Get one supplier scorecard period"

)

def get_supplier_scorecard_period(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SupplierScorecardPeriodRead:

    try:

        return SupplierScorecardPeriodRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=SupplierScorecardPeriodRead, summary="Update")

def update_supplier_scorecard_period(

    row_id: uuid.UUID, payload: SupplierScorecardPeriodUpdate, db: DbDep, business_id: BusinessDep

) -> SupplierScorecardPeriodRead:

    try:

        return SupplierScorecardPeriodRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_supplier_scorecard_period(

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
