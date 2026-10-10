"""Read-only HTTP surface for AdvanceTaxesAndCharges."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.advance_taxes_and_charges_domain.schemas.advance_taxes_and_charges import AdvanceTaxesAndChargesListResponse, AdvanceTaxesAndChargesRead

from app.accounts.advance_taxes_and_charges_domain.services.advance_taxes_and_charges_service import AdvanceTaxesAndChargesService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AdvanceTaxesAndChargesService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=AdvanceTaxesAndChargesListResponse, summary="List AdvanceTaxesAndCharges rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> AdvanceTaxesAndChargesListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return AdvanceTaxesAndChargesListResponse.from_result(

        page, [AdvanceTaxesAndChargesRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=AdvanceTaxesAndChargesRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> AdvanceTaxesAndChargesRead:

    try:

        return AdvanceTaxesAndChargesRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
