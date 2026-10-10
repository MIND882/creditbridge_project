"""Pydantic v2 schemas for JournalEntryTemplateAccount (child table, read-only API)."""



from __future__ import annotations



from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JournalEntryTemplateAccountCreate",

    "JournalEntryTemplateAccountRead",

    "JournalEntryTemplateAccountListResponse",

]





class JournalEntryTemplateAccountCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    account_id: uuid.UUID

    party_type: Optional[str] = None

    party: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None





class JournalEntryTemplateAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    account_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None





JournalEntryTemplateAccountListResponse = Page[JournalEntryTemplateAccountRead]
