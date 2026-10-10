"""Pydantic v2 schemas for POSSettings."""





from __future__ import annotations

from app.accounts.pos_settings_domain.models.pos_settings import (

    POSSettingsInvoiceType,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_field_domain.schemas.pos_field import (

    POSFieldCreate,

    POSFieldRead,

)

from app.accounts.pos_search_fields_domain.schemas.pos_search_fields import (

    POSSearchFieldsCreate,

    POSSearchFieldsRead,

)



__all__ = [

    "POSSettingsCreate",

    "POSSettingsUpdate",

    "POSSettingsRead",

    "POSSettingsListResponse",

]





class POSSettingsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    invoice_type: Optional[POSSettingsInvoiceType] = None

    post_change_gl_entries: Optional[bool] = None



    invoice_fields: list[POSFieldCreate] = []



    pos_search_fields: list[POSSearchFieldsCreate] = []





class POSSettingsCreate(POSSettingsBase):

    pass





class POSSettingsUpdate(InputSchema):

    """A partial update."""



    invoice_type: Optional[POSSettingsInvoiceType] = None

    post_change_gl_entries: Optional[bool] = None

    invoice_fields: Optional[list[POSFieldCreate]] = None

    pos_search_fields: Optional[list[POSSearchFieldsCreate]] = None





class POSSettingsRead(ReadSchema):

    id: uuid.UUID

    name: str

    invoice_type: Optional[POSSettingsInvoiceType] = None

    post_change_gl_entries: bool

    invoice_fields: list[POSFieldRead] = []

    pos_search_fields: list[POSSearchFieldsRead] = []





POSSettingsListResponse = Page[POSSettingsRead]
