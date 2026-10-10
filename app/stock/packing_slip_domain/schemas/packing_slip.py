"""Pydantic v2 schemas for PackingSlip."""





from __future__ import annotations

from app.stock.packing_slip_domain.models.packing_slip import (

    PackingSlipNamingSeries,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.stock.packing_slip_item_domain.schemas.packing_slip_item import (

    PackingSlipItemCreate,

    PackingSlipItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PackingSlipCreate",

    "PackingSlipUpdate",

    "PackingSlipRead",

    "PackingSlipListResponse",

]





class PackingSlipBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    delivery_note_id: uuid.UUID

    naming_series: PackingSlipNamingSeries

    from_case_no: int

    to_case_no: Optional[int] = None

    net_weight_pkg: Optional[Decimal] = None

    net_weight_uom_id: Optional[uuid.UUID] = None

    gross_weight_pkg: Optional[Decimal] = None

    gross_weight_uom_id: Optional[uuid.UUID] = None

    letter_head: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: list[PackingSlipItemCreate] = []





class PackingSlipCreate(PackingSlipBase):

    pass





class PackingSlipUpdate(InputSchema):

    """A partial update."""



    delivery_note_id: Optional[uuid.UUID] = None

    naming_series: Optional[PackingSlipNamingSeries] = None

    from_case_no: Optional[int] = None

    to_case_no: Optional[int] = None

    net_weight_pkg: Optional[Decimal] = None

    net_weight_uom_id: Optional[uuid.UUID] = None

    gross_weight_pkg: Optional[Decimal] = None

    gross_weight_uom_id: Optional[uuid.UUID] = None

    letter_head: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: Optional[list[PackingSlipItemCreate]] = None





class PackingSlipRead(ReadSchema):

    id: uuid.UUID

    name: str

    delivery_note_id: Optional[uuid.UUID] = None

    naming_series: Optional[PackingSlipNamingSeries] = None

    from_case_no: Optional[int] = None

    to_case_no: Optional[int] = None

    net_weight_pkg: Optional[Decimal] = None

    net_weight_uom_id: Optional[uuid.UUID] = None

    gross_weight_pkg: Optional[Decimal] = None

    gross_weight_uom_id: Optional[uuid.UUID] = None

    letter_head: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[PackingSlipItemRead] = []





PackingSlipListResponse = Page[PackingSlipRead]
