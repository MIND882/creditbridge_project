"""HTTP surface for Currency Exchange Settings Details -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.currency_exchange_settings_details_domain.schemas.currency_exchange_settings_details import (

    CurrencyExchangeSettingsDetailsListResponse,

    CurrencyExchangeSettingsDetailsRead,

)

from app.accounts.currency_exchange_settings_details_domain.services.currency_exchange_settings_details_service import CurrencyExchangeSettingsDetailsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = CurrencyExchangeSettingsDetailsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=CurrencyExchangeSettingsDetailsListResponse, summary="List currency exchange settings details rows")

def list_currency_exchange_settings_details(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> CurrencyExchangeSettingsDetailsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return CurrencyExchangeSettingsDetailsListResponse.from_result(

        page, [CurrencyExchangeSettingsDetailsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=CurrencyExchangeSettingsDetailsRead, summary="Get one currency exchange settings details row")

def get_currency_exchange_settings_details(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CurrencyExchangeSettingsDetailsRead:

    try:

        return CurrencyExchangeSettingsDetailsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
