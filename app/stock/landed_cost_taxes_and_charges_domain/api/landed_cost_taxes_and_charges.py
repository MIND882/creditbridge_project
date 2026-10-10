"""HTTP surface for Landed Cost Taxes and Charges -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.landed_cost_taxes_and_charges_domain.schemas.landed_cost_taxes_and_charges import (

    LandedCostTaxesAndChargesListResponse,

    LandedCostTaxesAndChargesRead,

)

from app.stock.landed_cost_taxes_and_charges_domain.services.landed_cost_taxes_and_charges_service import LandedCostTaxesAndChargesService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LandedCostTaxesAndChargesService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=LandedCostTaxesAndChargesListResponse, summary="List landed cost taxes and charges rows")

def list_landed_cost_taxes_and_charges(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> LandedCostTaxesAndChargesListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return LandedCostTaxesAndChargesListResponse.from_result(

        page, [LandedCostTaxesAndChargesRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=LandedCostTaxesAndChargesRead, summary="Get one landed cost taxes and charges row"

)

def get_landed_cost_taxes_and_charges(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LandedCostTaxesAndChargesRead:

    try:

        return LandedCostTaxesAndChargesRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
