"""Read-only HTTP surface for ItemWiseTaxDetail."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.item_wise_tax_detail_domain.schemas.item_wise_tax_detail import ItemWiseTaxDetailListResponse, ItemWiseTaxDetailRead

from app.accounts.item_wise_tax_detail_domain.services.item_wise_tax_detail_service import ItemWiseTaxDetailService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemWiseTaxDetailService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ItemWiseTaxDetailListResponse, summary="List ItemWiseTaxDetail rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    item_row: Optional[str] = Query(default=None),

) -> ItemWiseTaxDetailListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, item_row=item_row)

    return ItemWiseTaxDetailListResponse.from_result(

        page, [ItemWiseTaxDetailRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ItemWiseTaxDetailRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> ItemWiseTaxDetailRead:

    try:

        return ItemWiseTaxDetailRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
