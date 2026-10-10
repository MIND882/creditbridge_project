"""Pydantic v2 schemas for SalesTeam."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesTeamCreate",

    "SalesTeamRead",

    "SalesTeamListResponse",

]





class SalesTeamBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_person: str

    contact_no: Optional[str] = None

    allocated_percentage: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    commission_rate: Optional[Decimal] = None

    incentives: Optional[Decimal] = None





class SalesTeamCreate(SalesTeamBase):

    pass





class SalesTeamUpdate(InputSchema):

    """A partial update."""



    sales_person: Optional[str] = None

    contact_no: Optional[str] = None

    allocated_percentage: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    commission_rate: Optional[Decimal] = None

    incentives: Optional[Decimal] = None





class SalesTeamRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    sales_person: str

    contact_no: Optional[str] = None

    allocated_percentage: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    commission_rate: Optional[Decimal] = None

    incentives: Optional[Decimal] = None





SalesTeamListResponse = Page[SalesTeamRead]
