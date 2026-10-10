"""Pydantic v2 schemas for PartyAccount (child table, read-only API)."""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["PartyAccountCreate", "PartyAccountRead", "PartyAccountListResponse"]





class PartyAccountCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    party_account_of: Optional[str] = None

    account_id: Optional[uuid.UUID] = None

    advance_account_id: Optional[uuid.UUID] = None





class PartyAccountRead(ReadSchema):

    id: uuid.UUID

    party_account_of: Optional[str] = None

    account_id: Optional[uuid.UUID] = None

    advance_account_id: Optional[uuid.UUID] = None





PartyAccountListResponse = Page[PartyAccountRead]
