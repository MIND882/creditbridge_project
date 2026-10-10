"""HTTP surface for ModeOfPaymentAccount -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.mode_of_payment_account_domain.schemas.mode_of_payment_account import (

    ModeOfPaymentAccountListResponse,

    ModeOfPaymentAccountRead,

)

from app.accounts.mode_of_payment_account_domain.services.mode_of_payment_account_service import ModeOfPaymentAccountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ModeOfPaymentAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ModeOfPaymentAccountListResponse, summary="List mode of payment account rows")

def list_mode_of_payment_accounts(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ModeOfPaymentAccountListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ModeOfPaymentAccountListResponse.from_result(

        page, [ModeOfPaymentAccountRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ModeOfPaymentAccountRead, summary="Get one mode of payment account row"

)

def get_mode_of_payment_account(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ModeOfPaymentAccountRead:

    try:

        return ModeOfPaymentAccountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
