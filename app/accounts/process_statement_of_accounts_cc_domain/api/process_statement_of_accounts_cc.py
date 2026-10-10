"""HTTP surface for Process Statement Of Accounts Cc -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.process_statement_of_accounts_cc_domain.schemas.process_statement_of_accounts_cc import (

    ProcessStatementOfAccountsCcListResponse,

    ProcessStatementOfAccountsCcRead,

)

from app.accounts.process_statement_of_accounts_cc_domain.services.process_statement_of_accounts_cc_service import ProcessStatementOfAccountsCcService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ProcessStatementOfAccountsCcService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ProcessStatementOfAccountsCcListResponse, summary="List process statement of accounts cc rows")

def list_process_statement_of_accounts_cc(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ProcessStatementOfAccountsCcListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ProcessStatementOfAccountsCcListResponse.from_result(

        page, [ProcessStatementOfAccountsCcRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ProcessStatementOfAccountsCcRead, summary="Get one process statement of accounts cc row")

def get_process_statement_of_accounts_cc(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ProcessStatementOfAccountsCcRead:

    try:

        return ProcessStatementOfAccountsCcRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
