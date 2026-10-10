"""Pydantic v2 schemas for CustomerCreditLimit."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CustomerCreditLimitCreate",

    "CustomerCreditLimitRead",

    "CustomerCreditLimitListResponse",

]





class CustomerCreditLimitBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    credit_limit: Optional[Decimal] = None

    overdue_billing_threshold: Optional[Decimal] = None

    company: Optional[str] = None

    bypass_credit_limit_check: Optional[bool] = None





class CustomerCreditLimitCreate(CustomerCreditLimitBase):

    pass





class CustomerCreditLimitUpdate(InputSchema):

    """A partial update."""



    credit_limit: Optional[Decimal] = None

    overdue_billing_threshold: Optional[Decimal] = None

    company: Optional[str] = None

    bypass_credit_limit_check: Optional[bool] = None





class CustomerCreditLimitRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    credit_limit: Optional[Decimal] = None

    overdue_billing_threshold: Optional[Decimal] = None

    company: Optional[str] = None

    bypass_credit_limit_check: Optional[bool] = None





CustomerCreditLimitListResponse = Page[CustomerCreditLimitRead]
