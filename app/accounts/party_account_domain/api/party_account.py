"""

Read-only HTTP surface for PartyAccount.



Unlike the other child tables there is no ``parent_id`` filter: Customer and

Supplier are not converted yet, so rows are keyed on a party-type label.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.party_account_domain.schemas.party_account import (

    PartyAccountListResponse,

    PartyAccountRead,

)

from app.accounts.party_account_domain.services.party_account_service import PartyAccountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PartyAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PartyAccountListResponse, summary="List party accounts")

def list_party_accounts(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    party_account_of: Optional[str] = Query(default=None, max_length=140),

) -> PartyAccountListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, party_account_of=party_account_of

    )

    return PartyAccountListResponse.from_result(

        page, [PartyAccountRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PartyAccountRead, summary="Get one party account")

def get_party_account(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> PartyAccountRead:

    try:

        return PartyAccountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
