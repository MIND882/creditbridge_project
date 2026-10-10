"""Pydantic v2 schemas for BisectNodes."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BisectNodesCreate",

    "BisectNodesUpdate",

    "BisectNodesRead",

    "BisectNodesListResponse",

]





class BisectNodesBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    root: Optional[str] = None

    left_child: Optional[str] = None

    right_child: Optional[str] = None

    period_from_date: Optional[dt.datetime] = None

    period_to_date: Optional[dt.datetime] = None

    difference: Optional[Decimal] = None

    balance_sheet_summary: Optional[Decimal] = None

    profit_loss_summary: Optional[Decimal] = None

    generated: Optional[bool] = None





class BisectNodesCreate(BisectNodesBase):

    pass





class BisectNodesUpdate(InputSchema):

    """A partial update."""



    root: Optional[str] = None

    left_child: Optional[str] = None

    right_child: Optional[str] = None

    period_from_date: Optional[dt.datetime] = None

    period_to_date: Optional[dt.datetime] = None

    difference: Optional[Decimal] = None

    balance_sheet_summary: Optional[Decimal] = None

    profit_loss_summary: Optional[Decimal] = None

    generated: Optional[bool] = None





class BisectNodesRead(ReadSchema):

    id: uuid.UUID

    name: str

    root: Optional[str] = None

    left_child: Optional[str] = None

    right_child: Optional[str] = None

    period_from_date: Optional[dt.datetime] = None

    period_to_date: Optional[dt.datetime] = None

    difference: Optional[Decimal] = None

    balance_sheet_summary: Optional[Decimal] = None

    profit_loss_summary: Optional[Decimal] = None

    generated: bool





BisectNodesListResponse = Page[BisectNodesRead]
