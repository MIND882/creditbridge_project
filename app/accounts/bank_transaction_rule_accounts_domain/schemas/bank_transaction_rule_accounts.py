"""Pydantic v2 schemas for BankTransactionRuleAccount (child table, read-only API)."""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["BankTransactionRuleAccountCreate", "BankTransactionRuleAccountRead", "BankTransactionRuleAccountListResponse"]





class BankTransactionRuleAccountCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    account_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    debit: Optional[str] = None

    credit: Optional[str] = None

    user_remark: Optional[str] = None





class BankTransactionRuleAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    account_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    debit: Optional[str] = None

    credit: Optional[str] = None

    user_remark: Optional[str] = None





BankTransactionRuleAccountListResponse = Page[BankTransactionRuleAccountRead]
