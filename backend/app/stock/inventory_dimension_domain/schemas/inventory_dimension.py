"""Pydantic v2 schemas for InventoryDimension."""





from __future__ import annotations

from app.stock.inventory_dimension_domain.models.inventory_dimension import (

    InventoryDimensionTypeOfTransaction,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "InventoryDimensionCreate",

    "InventoryDimensionUpdate",

    "InventoryDimensionRead",

    "InventoryDimensionListResponse",

]





class InventoryDimensionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_document: str

    dimension_name: str

    document_type: Optional[str] = None

    istable: Optional[bool] = None

    condition: Optional[str] = None

    apply_to_all_doctypes: Optional[bool] = None

    target_fieldname: Optional[str] = None

    source_fieldname: Optional[str] = None

    type_of_transaction: Optional[InventoryDimensionTypeOfTransaction] = None

    fetch_from_parent: Optional[str] = None

    mandatory_depends_on: Optional[str] = None

    reqd: Optional[bool] = None

    validate_negative_stock: Optional[bool] = None





class InventoryDimensionCreate(InventoryDimensionBase):

    pass





class InventoryDimensionUpdate(InputSchema):

    """A partial update."""



    reference_document: Optional[str] = None

    dimension_name: Optional[str] = None

    document_type: Optional[str] = None

    istable: Optional[bool] = None

    condition: Optional[str] = None

    apply_to_all_doctypes: Optional[bool] = None

    target_fieldname: Optional[str] = None

    source_fieldname: Optional[str] = None

    type_of_transaction: Optional[InventoryDimensionTypeOfTransaction] = None

    fetch_from_parent: Optional[str] = None

    mandatory_depends_on: Optional[str] = None

    reqd: Optional[bool] = None

    validate_negative_stock: Optional[bool] = None





class InventoryDimensionRead(ReadSchema):

    id: uuid.UUID

    name: str

    reference_document: str

    dimension_name: str

    document_type: Optional[str] = None

    istable: Optional[bool] = None

    condition: Optional[str] = None

    apply_to_all_doctypes: Optional[bool] = None

    target_fieldname: Optional[str] = None

    source_fieldname: Optional[str] = None

    type_of_transaction: Optional[InventoryDimensionTypeOfTransaction] = None

    fetch_from_parent: Optional[str] = None

    mandatory_depends_on: Optional[str] = None

    reqd: Optional[bool] = None

    validate_negative_stock: Optional[bool] = None





InventoryDimensionListResponse = Page[InventoryDimensionRead]
