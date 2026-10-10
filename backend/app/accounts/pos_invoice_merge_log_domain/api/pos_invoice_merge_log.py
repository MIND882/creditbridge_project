"""HTTP surface for POS Invoice Merge Log."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.pos_invoice_merge_log_domain.schemas.pos_invoice_merge_log import (

        POSInvoiceMergeLogCreate,

    POSInvoiceMergeLogUpdate,

    POSInvoiceMergeLogRead,

    POSInvoiceMergeLogListResponse,

)

from app.accounts.pos_invoice_merge_log_domain.services.pos_invoice_merge_log_service import POSInvoiceMergeLogService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = POSInvoiceMergeLogService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=POSInvoiceMergeLogRead, status_code=status.HTTP_201_CREATED,

    summary="Create a pos invoice merge log",

)

def create_pos_invoice_merge_log(

    payload: POSInvoiceMergeLogCreate, db: DbDep, business_id: BusinessDep

) -> POSInvoiceMergeLogRead:

    try:

        return POSInvoiceMergeLogRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=POSInvoiceMergeLogListResponse, summary="List pos invoice merge logs")

def list_pos_invoice_merge_log(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> POSInvoiceMergeLogListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return POSInvoiceMergeLogListResponse.from_result(

        page, [POSInvoiceMergeLogRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=POSInvoiceMergeLogRead, summary="Get one pos invoice merge log"

)

def get_pos_invoice_merge_log(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> POSInvoiceMergeLogRead:

    try:

        return POSInvoiceMergeLogRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=POSInvoiceMergeLogRead, summary="Update")

def update_pos_invoice_merge_log(

    row_id: uuid.UUID, payload: POSInvoiceMergeLogUpdate, db: DbDep, business_id: BusinessDep

) -> POSInvoiceMergeLogRead:

    try:

        return POSInvoiceMergeLogRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_pos_invoice_merge_log(

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





@router.post("/{row_id}/submit", response_model=POSInvoiceMergeLogRead, summary="Submit")

def submit_pos_invoice_merge_log(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> POSInvoiceMergeLogRead:

    try:

        return POSInvoiceMergeLogRead.model_validate(_service.submit(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=POSInvoiceMergeLogRead, summary="Cancel")

def cancel_pos_invoice_merge_log(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> POSInvoiceMergeLogRead:

    try:

        return POSInvoiceMergeLogRead.model_validate(_service.cancel(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
