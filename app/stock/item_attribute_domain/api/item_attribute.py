"""HTTP surface for Item Attribute."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.stock.item_attribute_domain.schemas.item_attribute import (

    ItemAttributeCreate,

    ItemAttributeUpdate,

    ItemAttributeRead,

    ItemAttributeListResponse,

)

from app.stock.item_attribute_domain.services.item_attribute_service import ItemAttributeService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemAttributeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=ItemAttributeRead, status_code=status.HTTP_201_CREATED,

    summary="Create a item attribute",

)

def create_item_attribute(

    payload: ItemAttributeCreate, db: DbDep, business_id: BusinessDep

) -> ItemAttributeRead:

    try:

        return ItemAttributeRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=ItemAttributeListResponse, summary="List item attributes")

def list_item_attribute(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> ItemAttributeListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return ItemAttributeListResponse.from_result(

        page, [ItemAttributeRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ItemAttributeRead, summary="Get one item attribute"

)

def get_item_attribute(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemAttributeRead:

    try:

        return ItemAttributeRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=ItemAttributeRead, summary="Update")

def update_item_attribute(

    row_id: uuid.UUID, payload: ItemAttributeUpdate, db: DbDep, business_id: BusinessDep

) -> ItemAttributeRead:

    try:

        return ItemAttributeRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_item_attribute(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to NoneType and then rejects for a

    # 204 at import time.

    try:

        _service.delete(db, business_id, row_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
