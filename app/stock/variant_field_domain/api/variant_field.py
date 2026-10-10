"""HTTP surface for Variant Field -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.variant_field_domain.schemas.variant_field import (

    VariantFieldListResponse,

    VariantFieldRead,

)

from app.stock.variant_field_domain.services.variant_field_service import VariantFieldService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = VariantFieldService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=VariantFieldListResponse, summary="List variant field rows")

def list_variant_field(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> VariantFieldListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return VariantFieldListResponse.from_result(

        page, [VariantFieldRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=VariantFieldRead, summary="Get one variant field row"

)

def get_variant_field(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> VariantFieldRead:

    try:

        return VariantFieldRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
