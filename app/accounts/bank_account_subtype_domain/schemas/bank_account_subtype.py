"""Pydantic v2 schemas for Bank Account Subtype."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["BankAccountSubtypeCreate", "BankAccountSubtypeUpdate", "BankAccountSubtypeRead", "BankAccountSubtypeListResponse"]





class BankAccountSubtypeCreate(InputSchema):

    account_subtype: Annotated[str, Field(min_length=1, max_length=140)]





class BankAccountSubtypeUpdate(InputSchema):

    account_subtype: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None





class BankAccountSubtypeRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    account_subtype: str

    created_at: datetime

    updated_at: datetime





BankAccountSubtypeListResponse = Page[BankAccountSubtypeRead]
