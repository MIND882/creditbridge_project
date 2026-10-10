"""Pydantic v2 schemas for AdvanceTaxesAndCharges (child table, read-only API)."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.accounts.tax_enums import AddDeductTax, ChargeType

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "AdvanceTaxesAndChargesCreate",

    "AdvanceTaxesAndChargesRead",

    "AdvanceTaxesAndChargesListResponse",

]





class AdvanceTaxesAndChargesCreate(InputSchema):

    """Accepted only nested inside a Payment Entry create/update payload."""



    charge_type: ChargeType

    add_deduct_tax: AddDeductTax

    row_id: Optional[str] = None

    account_head_id: uuid.UUID

    cost_center_id: Optional[uuid.UUID] = None

    description: str

    project: Optional[str] = None

    rate: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    total: Optional[Decimal] = None

    base_tax_amount: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    included_in_paid_amount: Optional[bool] = False

    currency: Optional[str] = None

    net_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    set_by_item_tax_template: Optional[bool] = False

    is_tax_withholding_account: Optional[bool] = False





class AdvanceTaxesAndChargesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    charge_type: Optional[ChargeType] = None

    add_deduct_tax: Optional[AddDeductTax] = None

    row_id: Optional[str] = None

    account_head_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    project: Optional[str] = None

    rate: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    total: Optional[Decimal] = None

    base_tax_amount: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    included_in_paid_amount: bool

    currency: Optional[str] = None

    net_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    set_by_item_tax_template: bool

    is_tax_withholding_account: bool





AdvanceTaxesAndChargesListResponse = Page[AdvanceTaxesAndChargesRead]
