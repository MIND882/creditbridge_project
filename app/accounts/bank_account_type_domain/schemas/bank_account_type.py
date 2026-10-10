"""Pydantic v2 schemas for Bank Account Type."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["BankAccountTypeCreate", "BankAccountTypeUpdate", "BankAccountTypeRead", "BankAccountTypeListResponse"]





class BankAccountTypeCreate(InputSchema):

    account_type: Annotated[str, Field(min_length=1, max_length=140)]





class BankAccountTypeUpdate(InputSchema):

    account_type: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None





class BankAccountTypeRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    account_type: str

    created_at: datetime

    updated_at: datetime





BankAccountTypeListResponse = Page[BankAccountTypeRead]
