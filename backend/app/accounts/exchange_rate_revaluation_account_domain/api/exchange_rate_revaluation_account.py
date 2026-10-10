"""HTTP surface for Exchange Rate Revaluation Account -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.exchange_rate_revaluation_account_domain.schemas.exchange_rate_revaluation_account import (

    ExchangeRateRevaluationAccountListResponse,

    ExchangeRateRevaluationAccountRead,

)

from app.accounts.exchange_rate_revaluation_account_domain.services.exchange_rate_revaluation_account_service import ExchangeRateRevaluationAccountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ExchangeRateRevaluationAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ExchangeRateRevaluationAccountListResponse, summary="List exchange rate revaluation account rows")

def list_exchange_rate_revaluation_account(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ExchangeRateRevaluationAccountListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ExchangeRateRevaluationAccountListResponse.from_result(

        page, [ExchangeRateRevaluationAccountRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ExchangeRateRevaluationAccountRead, summary="Get one exchange rate revaluation account row")

def get_exchange_rate_revaluation_account(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ExchangeRateRevaluationAccountRead:

    try:

        return ExchangeRateRevaluationAccountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
