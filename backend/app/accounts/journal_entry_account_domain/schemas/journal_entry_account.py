"""Pydantic v2 schemas for JournalEntryAccount (child table, read-only API)."""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["JournalEntryAccountCreate", "JournalEntryAccountRead", "JournalEntryAccountListResponse"]





class JournalEntryAccountCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    account_id: uuid.UUID

    account_type: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    account_currency: Optional[str] = None

    exchange_rate: Optional[float] = None

    debit_in_account_currency: Optional[Decimal] = None

    debit: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None

    credit: Optional[Decimal] = None

    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    reference_due_date: Optional[dt.date] = None

    project: Optional[str] = None

    is_advance: Optional[str] = None

    user_remark: Optional[str] = None

    against_account: Optional[str] = None

    bank_account_id: Optional[uuid.UUID] = None

    reference_detail_no: Optional[str] = None





class JournalEntryAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    account_id: uuid.UUID

    account_type: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    account_currency: Optional[str] = None

    exchange_rate: Optional[float] = None

    debit_in_account_currency: Optional[Decimal] = None

    debit: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None

    credit: Optional[Decimal] = None

    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    reference_due_date: Optional[dt.date] = None

    project: Optional[str] = None

    is_advance: Optional[str] = None

    user_remark: Optional[str] = None

    against_account: Optional[str] = None

    bank_account_id: Optional[uuid.UUID] = None

    reference_detail_no: Optional[str] = None





JournalEntryAccountListResponse = Page[JournalEntryAccountRead]
