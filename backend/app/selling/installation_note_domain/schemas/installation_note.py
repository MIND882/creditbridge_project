"""Pydantic v2 schemas for InstallationNote."""





from __future__ import annotations

from app.selling.installation_note_domain.models.installation_note import (

    InstallationNoteNamingSeries,

    InstallationNoteStatus,

)

from typing import Optional

import datetime as dt

import uuid



from app.selling.installation_note_item_domain.schemas.installation_note_item import (

    InstallationNoteItemCreate,

    InstallationNoteItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "InstallationNoteCreate",

    "InstallationNoteUpdate",

    "InstallationNoteRead",

    "InstallationNoteListResponse",

]





class InstallationNoteBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: InstallationNoteNamingSeries

    customer_id: uuid.UUID

    customer_address: Optional[str] = None

    contact_person: Optional[str] = None

    customer_name: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    territory: str

    customer_group: Optional[str] = None

    inst_date: dt.date

    inst_time: Optional[dt.time] = None

    status: InstallationNoteStatus

    company: str

    amended_from_id: Optional[uuid.UUID] = None

    remarks: Optional[str] = None

    project: Optional[str] = None

    items: list[InstallationNoteItemCreate] = []





class InstallationNoteCreate(InstallationNoteBase):

    pass





class InstallationNoteUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[InstallationNoteNamingSeries] = None

    customer_id: Optional[uuid.UUID] = None

    customer_address: Optional[str] = None

    contact_person: Optional[str] = None

    customer_name: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    territory: Optional[str] = None

    customer_group: Optional[str] = None

    inst_date: Optional[dt.date] = None

    inst_time: Optional[dt.time] = None

    status: Optional[InstallationNoteStatus] = None

    company: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    remarks: Optional[str] = None

    project: Optional[str] = None

    items: Optional[list[InstallationNoteItemCreate]] = None





class InstallationNoteRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[InstallationNoteNamingSeries] = None

    customer_id: Optional[uuid.UUID] = None

    customer_address: Optional[str] = None

    contact_person: Optional[str] = None

    customer_name: Optional[str] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    contact_email: Optional[str] = None

    territory: str

    customer_group: Optional[str] = None

    inst_date: Optional[dt.date] = None

    inst_time: Optional[dt.time] = None

    status: Optional[InstallationNoteStatus] = None

    company: str

    amended_from_id: Optional[uuid.UUID] = None

    remarks: Optional[str] = None

    project: Optional[str] = None

    items: list[InstallationNoteItemRead] = []





InstallationNoteListResponse = Page[InstallationNoteRead]
