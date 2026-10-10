"""Pydantic v2 schemas for ProcessStatementOfAccountsCustomer."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessStatementOfAccountsCustomerCreate",

    "ProcessStatementOfAccountsCustomerRead",

    "ProcessStatementOfAccountsCustomerListResponse",

]





class ProcessStatementOfAccountsCustomerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    customer: str

    primary_email: Optional[str] = None

    billing_email: Optional[str] = None

    customer_name: Optional[str] = None





class ProcessStatementOfAccountsCustomerCreate(ProcessStatementOfAccountsCustomerBase):

    """Accepted only nested inside the parent payload."""

    pass





class ProcessStatementOfAccountsCustomerRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    customer: str

    primary_email: Optional[str] = None

    billing_email: Optional[str] = None

    customer_name: Optional[str] = None





ProcessStatementOfAccountsCustomerListResponse = Page[ProcessStatementOfAccountsCustomerRead]
