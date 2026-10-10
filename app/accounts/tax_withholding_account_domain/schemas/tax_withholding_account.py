"""Pydantic v2 schemas for TaxWithholdingAccount (child table, read-only API)."""



from __future__ import annotations



import uuid

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "TaxWithholdingAccountCreate",

    "TaxWithholdingAccountRead",

    "TaxWithholdingAccountListResponse",

]





class TaxWithholdingAccountCreate(InputSchema):

    """

    Accepted only nested inside the parent's create/update payload.



    Upstream carries a ``company`` here; tenancy is ``business_id``, which the

    core dependency supplies, so it is not accepted on input.

    """



    account_id: uuid.UUID





class TaxWithholdingAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    account_id: Optional[uuid.UUID] = None





TaxWithholdingAccountListResponse = Page[TaxWithholdingAccountRead]
