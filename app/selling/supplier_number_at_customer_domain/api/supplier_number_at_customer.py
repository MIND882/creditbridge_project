"""HTTP surface for Supplier Number At Customer -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.selling.supplier_number_at_customer_domain.schemas.supplier_number_at_customer import (

    SupplierNumberAtCustomerListResponse,

    SupplierNumberAtCustomerRead,

)

from app.selling.supplier_number_at_customer_domain.services.supplier_number_at_customer_service import SupplierNumberAtCustomerService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SupplierNumberAtCustomerService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SupplierNumberAtCustomerListResponse, summary="List supplier number at customer rows")

def list_supplier_number_at_customer(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SupplierNumberAtCustomerListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SupplierNumberAtCustomerListResponse.from_result(

        page, [SupplierNumberAtCustomerRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=SupplierNumberAtCustomerRead, summary="Get one supplier number at customer row"

)

def get_supplier_number_at_customer(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SupplierNumberAtCustomerRead:

    try:

        return SupplierNumberAtCustomerRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
