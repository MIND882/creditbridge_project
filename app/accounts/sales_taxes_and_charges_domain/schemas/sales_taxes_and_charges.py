"""Pydantic v2 schemas for SalesTaxesAndCharges (child table, read-only API)."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.accounts.tax_enums import ChargeType

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesTaxesAndChargesCreate",

    "SalesTaxesAndChargesRead",

    "SalesTaxesAndChargesListResponse",

]





class SalesTaxesAndChargesCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    charge_type: ChargeType

    row_id: Optional[str] = None

    account_head_id: uuid.UUID

    cost_center_id: Optional[uuid.UUID] = None

    description: str

    included_in_print_rate: Optional[bool] = False

    rate: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    total: Optional[Decimal] = None

    tax_amount_after_discount_amount: Optional[Decimal] = None

    base_tax_amount: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_tax_amount_after_discount_amount: Optional[Decimal] = None

    project: Optional[str] = None

    included_in_paid_amount: Optional[bool] = False

    dont_recompute_tax: Optional[bool] = False

    account_currency: Optional[str] = None

    net_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    set_by_item_tax_template: Optional[bool] = False

    is_tax_withholding_account: Optional[bool] = False





class SalesTaxesAndChargesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    charge_type: Optional[ChargeType] = None

    row_id: Optional[str] = None

    account_head_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    included_in_print_rate: bool

    rate: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    total: Optional[Decimal] = None

    tax_amount_after_discount_amount: Optional[Decimal] = None

    base_tax_amount: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_tax_amount_after_discount_amount: Optional[Decimal] = None

    project: Optional[str] = None

    included_in_paid_amount: bool

    dont_recompute_tax: bool

    account_currency: Optional[str] = None

    net_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    set_by_item_tax_template: bool

    is_tax_withholding_account: bool





SalesTaxesAndChargesListResponse = Page[SalesTaxesAndChargesRead]
