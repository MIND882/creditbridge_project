"""HTTP surface for Pegged Currency Details -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.pegged_currency_details_domain.schemas.pegged_currency_details import (

    PeggedCurrencyDetailsListResponse,

    PeggedCurrencyDetailsRead,

)

from app.accounts.pegged_currency_details_domain.services.pegged_currency_details_service import PeggedCurrencyDetailsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PeggedCurrencyDetailsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PeggedCurrencyDetailsListResponse, summary="List pegged currency details rows")

def list_pegged_currency_details(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PeggedCurrencyDetailsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PeggedCurrencyDetailsListResponse.from_result(

        page, [PeggedCurrencyDetailsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PeggedCurrencyDetailsRead, summary="Get one pegged currency details row")

def get_pegged_currency_details(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PeggedCurrencyDetailsRead:

    try:

        return PeggedCurrencyDetailsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
