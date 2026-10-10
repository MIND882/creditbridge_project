"""Pydantic v2 schemas for Accounting Period and its Closed Document child rows."""



from __future__ import annotations



import uuid

from datetime import date, datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "ClosedDocumentCreate",

    "ClosedDocumentRead",

    "AccountingPeriodCreate",

    "AccountingPeriodUpdate",

    "AccountingPeriodRead",

    "AccountingPeriodListResponse",

]





class ClosedDocumentCreate(InputSchema):

    document_type: Annotated[str, Field(min_length=1, max_length=140)]

    closed: bool = True





class ClosedDocumentRead(ReadSchema):

    id: uuid.UUID

    idx: int

    document_type: str

    closed: bool





class AccountingPeriodCreate(InputSchema):

    period_name: Annotated[str, Field(min_length=1, max_length=140)]

    start_date: date

    end_date: date

    disabled: bool = False

    exempted_role: Optional[Annotated[str, Field(max_length=140)]] = None

    closed_documents: list[ClosedDocumentCreate] = Field(default_factory=list)



    @field_validator("exempted_role", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingPeriodUpdate(InputSchema):

    period_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    disabled: Optional[bool] = None

    exempted_role: Optional[Annotated[str, Field(max_length=140)]] = None

    closed_documents: Optional[list[ClosedDocumentCreate]] = None



    @field_validator("exempted_role", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountingPeriodRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    period_name: str

    start_date: date

    end_date: date

    disabled: bool

    exempted_role: Optional[str] = None

    closed_documents: list[ClosedDocumentRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





AccountingPeriodListResponse = Page[AccountingPeriodRead]
