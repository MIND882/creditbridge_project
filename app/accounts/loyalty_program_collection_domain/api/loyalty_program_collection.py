"""HTTP surface for Loyalty Program Collection -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.loyalty_program_collection_domain.schemas.loyalty_program_collection import (

    LoyaltyProgramCollectionListResponse,

    LoyaltyProgramCollectionRead,

)

from app.accounts.loyalty_program_collection_domain.services.loyalty_program_collection_service import LoyaltyProgramCollectionService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LoyaltyProgramCollectionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=LoyaltyProgramCollectionListResponse, summary="List loyalty program collection rows")

def list_loyalty_program_collection(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> LoyaltyProgramCollectionListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return LoyaltyProgramCollectionListResponse.from_result(

        page, [LoyaltyProgramCollectionRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=LoyaltyProgramCollectionRead, summary="Get one loyalty program collection row")

def get_loyalty_program_collection(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LoyaltyProgramCollectionRead:

    try:

        return LoyaltyProgramCollectionRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
