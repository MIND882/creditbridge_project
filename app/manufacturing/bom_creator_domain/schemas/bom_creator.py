"""Pydantic v2 schemas for BomCreator."""





from __future__ import annotations

from app.manufacturing.bom_creator_domain.models.bom_creator import (

    BomCreatorRmCostAsPer,

    BomCreatorStatus,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.manufacturing.bom_creator_item_domain.schemas.bom_creator_item import (

    BomCreatorItemCreate,

    BomCreatorItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomCreatorCreate",

    "BomCreatorUpdate",

    "BomCreatorRead",

    "BomCreatorListResponse",

]





class BomCreatorBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    is_phantom: Optional[bool] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    qty: Decimal

    project: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    routing_id: Optional[uuid.UUID] = None

    rm_cost_as_per: BomCreatorRmCostAsPer

    set_rate_based_on_warehouse: Optional[bool] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    default_warehouse_id: Optional[uuid.UUID] = None

    company: str

    raw_material_cost: Optional[Decimal] = None

    remarks: Optional[str] = None

    status: Optional[BomCreatorStatus] = None

    error_log: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: list[BomCreatorItemCreate] = []





class BomCreatorCreate(BomCreatorBase):

    pass





class BomCreatorUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    is_phantom: Optional[bool] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    project: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    routing_id: Optional[uuid.UUID] = None

    rm_cost_as_per: Optional[BomCreatorRmCostAsPer] = None

    set_rate_based_on_warehouse: Optional[bool] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    default_warehouse_id: Optional[uuid.UUID] = None

    company: Optional[str] = None

    raw_material_cost: Optional[Decimal] = None

    remarks: Optional[str] = None

    status: Optional[BomCreatorStatus] = None

    error_log: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: Optional[list[BomCreatorItemCreate]] = None





class BomCreatorRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    is_phantom: Optional[bool] = None

    item_name: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    project: Optional[str] = None

    uom_id: Optional[uuid.UUID] = None

    routing_id: Optional[uuid.UUID] = None

    rm_cost_as_per: Optional[BomCreatorRmCostAsPer] = None

    set_rate_based_on_warehouse: Optional[bool] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    default_warehouse_id: Optional[uuid.UUID] = None

    company: str

    raw_material_cost: Optional[Decimal] = None

    remarks: Optional[str] = None

    status: Optional[BomCreatorStatus] = None

    error_log: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[BomCreatorItemRead] = []





BomCreatorListResponse = Page[BomCreatorRead]
