"""Pydantic v2 schemas for BankTransactionRuleDescriptionCondition (child table, read-only API)."""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["BankTransactionRuleDescriptionConditionCreate", "BankTransactionRuleDescriptionConditionRead", "BankTransactionRuleDescriptionConditionListResponse"]





class BankTransactionRuleDescriptionConditionCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    check: Annotated[str, Field(max_length=140)]

    value: Annotated[str, Field(max_length=140)]





class BankTransactionRuleDescriptionConditionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    check: str

    value: str





BankTransactionRuleDescriptionConditionListResponse = Page[BankTransactionRuleDescriptionConditionRead]
