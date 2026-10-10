"""Pydantic v2 schemas for OpeningInvoiceCreationTool."""





from __future__ import annotations

from app.accounts.opening_invoice_creation_tool_domain.models.opening_invoice_creation_tool import (

    OpeningInvoiceCreationToolInvoiceType,

)

from typing import Optional

import uuid



from app.accounts.opening_invoice_creation_tool_item_domain.schemas.opening_invoice_creation_tool_item import (

    OpeningInvoiceCreationToolItemCreate,

    OpeningInvoiceCreationToolItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.discounted_invoice_domain.schemas.discounted_invoice import (

    DiscountedInvoiceCreate,

    DiscountedInvoiceRead,

)



__all__ = [

    "OpeningInvoiceCreationToolCreate",

    "OpeningInvoiceCreationToolUpdate",

    "OpeningInvoiceCreationToolRead",

    "OpeningInvoiceCreationToolListResponse",

]





class OpeningInvoiceCreationToolBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    create_missing_party: Optional[bool] = None

    invoice_type: OpeningInvoiceCreationToolInvoiceType

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None



    invoices: list[OpeningInvoiceCreationToolItemCreate] = []





class OpeningInvoiceCreationToolCreate(OpeningInvoiceCreationToolBase):

    pass





class OpeningInvoiceCreationToolUpdate(InputSchema):

    """A partial update."""



    create_missing_party: Optional[bool] = None

    invoice_type: Optional[OpeningInvoiceCreationToolInvoiceType] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    invoices: Optional[list[OpeningInvoiceCreationToolItemCreate]] = None





class OpeningInvoiceCreationToolRead(ReadSchema):

    id: uuid.UUID

    name: str

    create_missing_party: bool

    invoice_type: OpeningInvoiceCreationToolInvoiceType

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    invoices: list[OpeningInvoiceCreationToolItemRead] = []





OpeningInvoiceCreationToolListResponse = Page[OpeningInvoiceCreationToolRead]
