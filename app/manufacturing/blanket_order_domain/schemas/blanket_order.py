"""Pydantic v2 schemas for BlanketOrder."""





from __future__ import annotations

from app.manufacturing.blanket_order_domain.models.blanket_order import (

    BlanketOrderNamingSeries,

    BlanketOrderBlanketOrderType,

)

from typing import Optional

import datetime as dt

import uuid



from app.manufacturing.blanket_order_item_domain.schemas.blanket_order_item import (

    BlanketOrderItemCreate,

    BlanketOrderItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BlanketOrderCreate",

    "BlanketOrderUpdate",

    "BlanketOrderRead",

    "BlanketOrderListResponse",

]





class BlanketOrderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: BlanketOrderNamingSeries

    blanket_order_type: BlanketOrderBlanketOrderType

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    order_no: Optional[str] = None

    order_date: Optional[dt.date] = None

    from_date: dt.date

    to_date: dt.date

    company: str

    amended_from_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    items: list[BlanketOrderItemCreate] = []





class BlanketOrderCreate(BlanketOrderBase):

    pass





class BlanketOrderUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[BlanketOrderNamingSeries] = None

    blanket_order_type: Optional[BlanketOrderBlanketOrderType] = None

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    order_no: Optional[str] = None

    order_date: Optional[dt.date] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    company: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    items: Optional[list[BlanketOrderItemCreate]] = None





class BlanketOrderRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[BlanketOrderNamingSeries] = None

    blanket_order_type: Optional[BlanketOrderBlanketOrderType] = None

    customer_id: Optional[uuid.UUID] = None

    customer_name: Optional[str] = None

    supplier_id: Optional[uuid.UUID] = None

    supplier_name: Optional[str] = None

    order_no: Optional[str] = None

    order_date: Optional[dt.date] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    company: str

    amended_from_id: Optional[uuid.UUID] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[BlanketOrderItemRead] = []





BlanketOrderListResponse = Page[BlanketOrderRead]
