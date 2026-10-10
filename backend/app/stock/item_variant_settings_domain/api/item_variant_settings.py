"""HTTP surface for Item Variant Settings.



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



from app.stock.item_variant_settings_domain.schemas.item_variant_settings import (

    ItemVariantSettingsRead,

    ItemVariantSettingsUpdate,

)

from app.stock.item_variant_settings_domain.services.item_variant_settings_service import ItemVariantSettingsService

from app.core.errors import DomainValidationError, to_http_exception

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemVariantSettingsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get(

    "", response_model=ItemVariantSettingsRead,

    summary="Get this tenant's item variant settings",

    description=(

        "Returns the single settings row for the current business, creating it "

        "with the upstream defaults if it has never been written."

    ),

)

def get_item_variant_settings(

    db: DbDep, business_id: BusinessDep

) -> ItemVariantSettingsRead:

    return ItemVariantSettingsRead.model_validate(

        _service.get_or_create(db, business_id)

    )





@router.patch(

    "", response_model=ItemVariantSettingsRead,

    summary="Update this tenant's item variant settings",

)

def update_item_variant_settings(

    payload: ItemVariantSettingsUpdate, db: DbDep, business_id: BusinessDep

) -> ItemVariantSettingsRead:

    try:

        return ItemVariantSettingsRead.model_validate(

            _service.update(db, business_id, payload)

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
