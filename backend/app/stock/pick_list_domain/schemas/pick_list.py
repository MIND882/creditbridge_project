"""Pydantic v2 schemas for PickList."""





from __future__ import annotations

from app.stock.pick_list_domain.models.pick_list import (

    PickListPurpose,

    PickListNamingSeries,

    PickListStatus,

    PickListDeliveryStatus,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.stock.pick_list_item_domain.schemas.pick_list_item import (

    PickListItemCreate,

    PickListItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PickListCreate",

    "PickListUpdate",

    "PickListRead",

    "PickListListResponse",

]





class PickListBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    parent_warehouse_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    work_order: Optional[str] = None

    for_qty: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    purpose: Optional[PickListPurpose] = None

    material_request_id: Optional[uuid.UUID] = None

    naming_series: PickListNamingSeries

    group_same_items: Optional[bool] = None

    scan_barcode: Optional[str] = None

    scan_mode: Optional[bool] = None

    prompt_qty: Optional[bool] = None

    customer_name: Optional[str] = None

    status: PickListStatus

    consider_rejected_warehouses: Optional[bool] = None

    pick_manually: Optional[bool] = None

    ignore_pricing_rule: Optional[bool] = None

    delivery_status: Optional[PickListDeliveryStatus] = None

    per_delivered: Optional[Decimal] = None

    locations: list[PickListItemCreate] = []





class PickListCreate(PickListBase):

    pass





class PickListUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    parent_warehouse_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    work_order: Optional[str] = None

    for_qty: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    purpose: Optional[PickListPurpose] = None

    material_request_id: Optional[uuid.UUID] = None

    naming_series: Optional[PickListNamingSeries] = None

    group_same_items: Optional[bool] = None

    scan_barcode: Optional[str] = None

    scan_mode: Optional[bool] = None

    prompt_qty: Optional[bool] = None

    customer_name: Optional[str] = None

    status: Optional[PickListStatus] = None

    consider_rejected_warehouses: Optional[bool] = None

    pick_manually: Optional[bool] = None

    ignore_pricing_rule: Optional[bool] = None

    delivery_status: Optional[PickListDeliveryStatus] = None

    per_delivered: Optional[Decimal] = None

    locations: Optional[list[PickListItemCreate]] = None





class PickListRead(ReadSchema):

    id: uuid.UUID

    name: str

    company: str

    parent_warehouse_id: Optional[uuid.UUID] = None

    customer: Optional[str] = None

    work_order: Optional[str] = None

    for_qty: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    purpose: Optional[PickListPurpose] = None

    material_request_id: Optional[uuid.UUID] = None

    naming_series: Optional[PickListNamingSeries] = None

    group_same_items: Optional[bool] = None

    scan_barcode: Optional[str] = None

    scan_mode: Optional[bool] = None

    prompt_qty: Optional[bool] = None

    customer_name: Optional[str] = None

    status: Optional[PickListStatus] = None

    consider_rejected_warehouses: Optional[bool] = None

    pick_manually: Optional[bool] = None

    ignore_pricing_rule: Optional[bool] = None

    delivery_status: Optional[PickListDeliveryStatus] = None

    per_delivered: Optional[Decimal] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    locations: list[PickListItemRead] = []





PickListListResponse = Page[PickListRead]
