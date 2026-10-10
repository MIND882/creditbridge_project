"""HTTP surface for Bank Statement Import Log."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_log_domain.schemas.bank_statement_import_log import (

        BankStatementImportLogCreate,

    BankStatementImportLogUpdate,

    BankStatementImportLogRead,

    BankStatementImportLogListResponse,

)

from app.accounts.bank_statement_import_log_domain.services.bank_statement_import_log_service import BankStatementImportLogService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankStatementImportLogService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=BankStatementImportLogRead, status_code=status.HTTP_201_CREATED,

    summary="Create a bank statement import log",

)

def create_bank_statement_import_log(

    payload: BankStatementImportLogCreate, db: DbDep, business_id: BusinessDep

) -> BankStatementImportLogRead:

    try:

        return BankStatementImportLogRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankStatementImportLogListResponse, summary="List bank statement import logs")

def list_bank_statement_import_log(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> BankStatementImportLogListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

    )

    return BankStatementImportLogListResponse.from_result(

        page, [BankStatementImportLogRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=BankStatementImportLogRead, summary="Get one bank statement import log"

)

def get_bank_statement_import_log(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankStatementImportLogRead:

    try:

        return BankStatementImportLogRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=BankStatementImportLogRead, summary="Update")

def update_bank_statement_import_log(

    row_id: uuid.UUID, payload: BankStatementImportLogUpdate, db: DbDep, business_id: BusinessDep

) -> BankStatementImportLogRead:

    try:

        return BankStatementImportLogRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_bank_statement_import_log(

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
