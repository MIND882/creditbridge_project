"""HTTP surface for Item Variant Attribute -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.item_variant_attribute_domain.schemas.item_variant_attribute import (

    ItemVariantAttributeListResponse,

    ItemVariantAttributeRead,

)

from app.stock.item_variant_attribute_domain.services.item_variant_attribute_service import ItemVariantAttributeService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemVariantAttributeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ItemVariantAttributeListResponse, summary="List item variant attribute rows")

def list_item_variant_attribute(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ItemVariantAttributeListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ItemVariantAttributeListResponse.from_result(

        page, [ItemVariantAttributeRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ItemVariantAttributeRead, summary="Get one item variant attribute row"

)

def get_item_variant_attribute(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemVariantAttributeRead:

    try:

        return ItemVariantAttributeRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
