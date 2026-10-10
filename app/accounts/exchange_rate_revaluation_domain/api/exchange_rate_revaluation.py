"""HTTP surface for Exchange Rate Revaluation."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.exchange_rate_revaluation_domain.schemas.exchange_rate_revaluation import (

        ExchangeRateRevaluationCreate,

    ExchangeRateRevaluationUpdate,

    ExchangeRateRevaluationRead,

    ExchangeRateRevaluationListResponse,

)

from app.accounts.exchange_rate_revaluation_domain.services.exchange_rate_revaluation_service import ExchangeRateRevaluationService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ExchangeRateRevaluationService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=ExchangeRateRevaluationRead, status_code=status.HTTP_201_CREATED,

    summary="Create a exchange rate revaluation",

)

def create_exchange_rate_revaluation(

    payload: ExchangeRateRevaluationCreate, db: DbDep, business_id: BusinessDep

) -> ExchangeRateRevaluationRead:

    try:

        return ExchangeRateRevaluationRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=ExchangeRateRevaluationListResponse, summary="List exchange rate revaluations")

def list_exchange_rate_revaluation(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> ExchangeRateRevaluationListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return ExchangeRateRevaluationListResponse.from_result(

        page, [ExchangeRateRevaluationRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ExchangeRateRevaluationRead, summary="Get one exchange rate revaluation"

)

def get_exchange_rate_revaluation(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ExchangeRateRevaluationRead:

    try:

        return ExchangeRateRevaluationRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=ExchangeRateRevaluationRead, summary="Update")

def update_exchange_rate_revaluation(

    row_id: uuid.UUID, payload: ExchangeRateRevaluationUpdate, db: DbDep, business_id: BusinessDep

) -> ExchangeRateRevaluationRead:

    try:

        return ExchangeRateRevaluationRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_exchange_rate_revaluation(

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





@router.post("/{row_id}/submit", response_model=ExchangeRateRevaluationRead, summary="Submit")

def submit_exchange_rate_revaluation(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ExchangeRateRevaluationRead:

    try:

        return ExchangeRateRevaluationRead.model_validate(_service.submit(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=ExchangeRateRevaluationRead, summary="Cancel")

def cancel_exchange_rate_revaluation(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ExchangeRateRevaluationRead:

    try:

        return ExchangeRateRevaluationRead.model_validate(_service.cancel(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
