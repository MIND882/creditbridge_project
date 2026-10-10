"""Pydantic v2 schemas for BisectAccountingStatements."""





from __future__ import annotations

from app.accounts.bisect_accounting_statements_domain.models.bisect_accounting_statements import (

    BisectAccountingStatementsAlgorithm,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BisectAccountingStatementsCreate",

    "BisectAccountingStatementsUpdate",

    "BisectAccountingStatementsRead",

    "BisectAccountingStatementsListResponse",

]





class BisectAccountingStatementsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    from_date: Optional[dt.datetime] = None

    to_date: Optional[dt.datetime] = None

    algorithm: Optional[BisectAccountingStatementsAlgorithm] = None

    current_node: Optional[str] = None

    current_from_date: Optional[dt.datetime] = None

    current_to_date: Optional[dt.datetime] = None

    p_l_summary: Optional[Decimal] = None

    b_s_summary: Optional[Decimal] = None

    difference: Optional[Decimal] = None





class BisectAccountingStatementsCreate(BisectAccountingStatementsBase):

    pass





class BisectAccountingStatementsUpdate(InputSchema):

    """A partial update."""



    from_date: Optional[dt.datetime] = None

    to_date: Optional[dt.datetime] = None

    algorithm: Optional[BisectAccountingStatementsAlgorithm] = None

    current_node: Optional[str] = None

    current_from_date: Optional[dt.datetime] = None

    current_to_date: Optional[dt.datetime] = None

    p_l_summary: Optional[Decimal] = None

    b_s_summary: Optional[Decimal] = None

    difference: Optional[Decimal] = None





class BisectAccountingStatementsRead(ReadSchema):

    id: uuid.UUID

    name: str

    from_date: Optional[dt.datetime] = None

    to_date: Optional[dt.datetime] = None

    algorithm: Optional[BisectAccountingStatementsAlgorithm] = None

    current_node: Optional[str] = None

    current_from_date: Optional[dt.datetime] = None

    current_to_date: Optional[dt.datetime] = None

    p_l_summary: Optional[Decimal] = None

    b_s_summary: Optional[Decimal] = None

    difference: Optional[Decimal] = None





BisectAccountingStatementsListResponse = Page[BisectAccountingStatementsRead]
