"""HTTP surface for UOM Conversion Detail -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.uom_conversion_detail_domain.schemas.uom_conversion_detail import (

    UomConversionDetailListResponse,

    UomConversionDetailRead,

)

from app.stock.uom_conversion_detail_domain.services.uom_conversion_detail_service import UomConversionDetailService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = UomConversionDetailService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=UomConversionDetailListResponse, summary="List uom conversion detail rows")

def list_uom_conversion_detail(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> UomConversionDetailListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return UomConversionDetailListResponse.from_result(

        page, [UomConversionDetailRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=UomConversionDetailRead, summary="Get one uom conversion detail row"

)

def get_uom_conversion_detail(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> UomConversionDetailRead:

    try:

        return UomConversionDetailRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
