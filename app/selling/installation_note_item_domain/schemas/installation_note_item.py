"""Pydantic v2 schemas for InstallationNoteItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "InstallationNoteItemCreate",

    "InstallationNoteItemRead",

    "InstallationNoteItemListResponse",

]





class InstallationNoteItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    serial_no: Optional[str] = None

    qty: Decimal

    description: Optional[str] = None

    prevdoc_detail_docname: Optional[str] = None

    prevdoc_docname: Optional[str] = None

    prevdoc_doctype: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None





class InstallationNoteItemCreate(InstallationNoteItemBase):

    pass





class InstallationNoteItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    qty: Optional[Decimal] = None

    description: Optional[str] = None

    prevdoc_detail_docname: Optional[str] = None

    prevdoc_docname: Optional[str] = None

    prevdoc_doctype: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None





class InstallationNoteItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    serial_no: Optional[str] = None

    qty: Optional[Decimal] = None

    description: Optional[str] = None

    prevdoc_detail_docname: Optional[str] = None

    prevdoc_docname: Optional[str] = None

    prevdoc_doctype: Optional[str] = None

    serial_and_batch_bundle_id: Optional[uuid.UUID] = None





InstallationNoteItemListResponse = Page[InstallationNoteItemRead]
