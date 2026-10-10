"""HTTP surface for Quick Stock Balance.



**Not the usual six endpoints.** Upstream this is a Frappe Single -- one document

per site -- so here there is one row per tenant and no collection to address:



    GET   /     the tenant's settings, created with defaults on first read

    PATCH /     partial update of that row



There is no ``POST /`` (nothing to create), no ``GET /{id}`` (the tenant *is* the

identity), and no ``DELETE /`` (settings are not deleted, they are reset by

patching fields back).

"""



from __future__ import annotations



import uuid

from typing import Annotated



from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session



from app.stock.quick_stock_balance_domain.schemas.quick_stock_balance import (

    QuickStockBalanceRead,

    QuickStockBalanceUpdate,

)

from app.stock.quick_stock_balance_domain.services.quick_stock_balance_service import QuickStockBalanceService

from app.core.errors import DomainValidationError, to_http_exception

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = QuickStockBalanceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get(

    "", response_model=QuickStockBalanceRead,

    summary="Get this tenant's quick stock balance",

    description=(

        "Returns the single settings row for the current business, creating it "

        "with the upstream defaults if it has never been written."

    ),

)

def get_quick_stock_balance(

    db: DbDep, business_id: BusinessDep

) -> QuickStockBalanceRead:

    return QuickStockBalanceRead.model_validate(

        _service.get_or_create(db, business_id)

    )





@router.patch(

    "", response_model=QuickStockBalanceRead,

    summary="Update this tenant's quick stock balance",

)

def update_quick_stock_balance(

    payload: QuickStockBalanceUpdate, db: DbDep, business_id: BusinessDep

) -> QuickStockBalanceRead:

    try:

        return QuickStockBalanceRead.model_validate(

            _service.update(db, business_id, payload)

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
