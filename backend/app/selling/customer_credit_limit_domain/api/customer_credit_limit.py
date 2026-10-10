"""HTTP surface for Customer Credit Limit -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.selling.customer_credit_limit_domain.schemas.customer_credit_limit import (

    CustomerCreditLimitListResponse,

    CustomerCreditLimitRead,

)

from app.selling.customer_credit_limit_domain.services.customer_credit_limit_service import CustomerCreditLimitService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = CustomerCreditLimitService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=CustomerCreditLimitListResponse, summary="List customer credit limit rows")

def list_customer_credit_limit(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> CustomerCreditLimitListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return CustomerCreditLimitListResponse.from_result(

        page, [CustomerCreditLimitRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=CustomerCreditLimitRead, summary="Get one customer credit limit row"

)

def get_customer_credit_limit(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CustomerCreditLimitRead:

    try:

        return CustomerCreditLimitRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
