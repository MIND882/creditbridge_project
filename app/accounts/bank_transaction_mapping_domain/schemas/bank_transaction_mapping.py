"""Pydantic v2 schemas for Bank Transaction Mapping (a child table of Bank)."""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = ["BankTransactionMappingCreate", "BankTransactionMappingUpdate", "BankTransactionMappingRead", "BankTransactionMappingListResponse"]





class BankTransactionMappingCreate(InputSchema):

    bank_transaction_field: str

    file_field: str









class BankTransactionMappingUpdate(InputSchema):

    bank_transaction_field: Optional[str] = None

    file_field: Optional[str] = None









class BankTransactionMappingRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    parent_id: Optional[uuid.UUID] = None

    idx: int

    bank_transaction_field: str

    file_field: str

    created_at: datetime

    updated_at: datetime





BankTransactionMappingListResponse = Page[BankTransactionMappingRead]
