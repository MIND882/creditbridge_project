"""Pydantic v2 schemas for Finance Book."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["FinanceBookCreate", "FinanceBookUpdate", "FinanceBookRead", "FinanceBookListResponse"]





class FinanceBookCreate(InputSchema):

    finance_book_name: Annotated[str, Field(min_length=1, max_length=140)]





class FinanceBookUpdate(InputSchema):

    finance_book_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None





class FinanceBookRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    finance_book_name: str

    created_at: datetime

    updated_at: datetime





FinanceBookListResponse = Page[FinanceBookRead]
