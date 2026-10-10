"""Pydantic v2 schemas for Bank."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "BankTransactionMappingCreate",

    "BankTransactionMappingRead",

    "BankCreate",

    "BankUpdate",

    "BankRead",

    "BankListResponse",

]





class BankTransactionMappingCreate(InputSchema):

    """Maps a column in an imported statement file onto a Bank Transaction field."""



    bank_transaction_field: Annotated[str, Field(min_length=1, max_length=140)]

    file_field: Annotated[str, Field(min_length=1, max_length=140)]





class BankTransactionMappingRead(ReadSchema):

    id: uuid.UUID

    idx: int

    bank_transaction_field: str

    file_field: str





class BankCreate(InputSchema):

    bank_name: Annotated[str, Field(min_length=1, max_length=140)]

    swift_number: Optional[Annotated[str, Field(max_length=140)]] = None

    website: Optional[Annotated[str, Field(max_length=140)]] = None

    plaid_access_token: Optional[Annotated[str, Field(max_length=140)]] = None

    bank_transaction_mapping: list[BankTransactionMappingCreate] = Field(default_factory=list)



    @field_validator("swift_number", "website", "plaid_access_token", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankUpdate(InputSchema):

    bank_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    swift_number: Optional[Annotated[str, Field(max_length=140)]] = None

    website: Optional[Annotated[str, Field(max_length=140)]] = None

    plaid_access_token: Optional[Annotated[str, Field(max_length=140)]] = None

    bank_transaction_mapping: Optional[list[BankTransactionMappingCreate]] = None



    @field_validator("swift_number", "website", "plaid_access_token", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankRead(ReadSchema):

    """

    Note ``plaid_access_token`` is intentionally absent.



    It is a third-party credential; exposing it on a GET would put a live

    Plaid token in every response body, log and browser cache.

    """



    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    bank_name: str

    swift_number: Optional[str] = None

    website: Optional[str] = None

    bank_transaction_mapping: list[BankTransactionMappingRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





BankListResponse = Page[BankRead]
