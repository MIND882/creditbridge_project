"""HTTP surface for Process Statement Of Accounts Customer -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.process_statement_of_accounts_customer_domain.schemas.process_statement_of_accounts_customer import (

    ProcessStatementOfAccountsCustomerListResponse,

    ProcessStatementOfAccountsCustomerRead,

)

from app.accounts.process_statement_of_accounts_customer_domain.services.process_statement_of_accounts_customer_service import ProcessStatementOfAccountsCustomerService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ProcessStatementOfAccountsCustomerService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ProcessStatementOfAccountsCustomerListResponse, summary="List process statement of accounts customer rows")

def list_process_statement_of_accounts_customer(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ProcessStatementOfAccountsCustomerListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ProcessStatementOfAccountsCustomerListResponse.from_result(

        page, [ProcessStatementOfAccountsCustomerRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ProcessStatementOfAccountsCustomerRead, summary="Get one process statement of accounts customer row")

def get_process_statement_of_accounts_customer(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ProcessStatementOfAccountsCustomerRead:

    try:

        return ProcessStatementOfAccountsCustomerRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
