"""HTTP surface for Bank Statement Import Log Column Map -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_log_column_map_domain.schemas.bank_statement_import_log_column_map import (

    BankStatementImportLogColumnMapListResponse,

    BankStatementImportLogColumnMapRead,

)

from app.accounts.bank_statement_import_log_column_map_domain.services.bank_statement_import_log_column_map_service import BankStatementImportLogColumnMapService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankStatementImportLogColumnMapService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=BankStatementImportLogColumnMapListResponse, summary="List bank statement import log column map rows")

def list_bank_statement_import_log_column_map(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> BankStatementImportLogColumnMapListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return BankStatementImportLogColumnMapListResponse.from_result(

        page, [BankStatementImportLogColumnMapRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=BankStatementImportLogColumnMapRead, summary="Get one bank statement import log column map row")

def get_bank_statement_import_log_column_map(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankStatementImportLogColumnMapRead:

    try:

        return BankStatementImportLogColumnMapRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
