"""Pydantic v2 schemas for LandedCostTaxesAndCharges."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LandedCostTaxesAndChargesCreate",

    "LandedCostTaxesAndChargesRead",

    "LandedCostTaxesAndChargesListResponse",

]





class LandedCostTaxesAndChargesBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    description: str

    amount: Decimal

    expense_account_id: Optional[uuid.UUID] = None

    account_currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    has_corrective_cost: Optional[bool] = None

    has_operating_cost: Optional[bool] = None

    operation_id: Optional[str] = None

    qty: Optional[Decimal] = None

    operating_component: Optional[str] = None





class LandedCostTaxesAndChargesCreate(LandedCostTaxesAndChargesBase):

    pass





class LandedCostTaxesAndChargesUpdate(InputSchema):

    """A partial update."""



    description: Optional[str] = None

    amount: Optional[Decimal] = None

    expense_account_id: Optional[uuid.UUID] = None

    account_currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    has_corrective_cost: Optional[bool] = None

    has_operating_cost: Optional[bool] = None

    operation_id: Optional[str] = None

    qty: Optional[Decimal] = None

    operating_component: Optional[str] = None





class LandedCostTaxesAndChargesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    description: str

    amount: Optional[Decimal] = None

    expense_account_id: Optional[uuid.UUID] = None

    account_currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None

    base_amount: Optional[Decimal] = None

    has_corrective_cost: Optional[bool] = None

    has_operating_cost: Optional[bool] = None

    operation_id: Optional[str] = None

    qty: Optional[Decimal] = None

    operating_component: Optional[str] = None





LandedCostTaxesAndChargesListResponse = Page[LandedCostTaxesAndChargesRead]
