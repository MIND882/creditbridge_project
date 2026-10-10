"""HTTP surface for Supplier Group Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.supplier_group_item_domain.schemas.supplier_group_item import (

    SupplierGroupItemListResponse,

    SupplierGroupItemRead,

)

from app.accounts.supplier_group_item_domain.services.supplier_group_item_service import SupplierGroupItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SupplierGroupItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SupplierGroupItemListResponse, summary="List supplier group item rows")

def list_supplier_group_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SupplierGroupItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SupplierGroupItemListResponse.from_result(

        page, [SupplierGroupItemRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=SupplierGroupItemRead, summary="Get one supplier group item row")

def get_supplier_group_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SupplierGroupItemRead:

    try:

        return SupplierGroupItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
