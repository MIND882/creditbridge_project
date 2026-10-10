"""Pydantic v2 schemas for PurchaseTaxesAndCharges (child table, read-only API)."""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.accounts.tax_enums import AddDeductTax, ChargeType, PurchaseTaxCategory

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseTaxesAndChargesCreate",

    "PurchaseTaxesAndChargesRead",

    "PurchaseTaxesAndChargesListResponse",

]





class PurchaseTaxesAndChargesCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    category: Optional[PurchaseTaxCategory] = PurchaseTaxCategory.TOTAL

    add_deduct_tax: Optional[AddDeductTax] = AddDeductTax.ADD

    charge_type: Optional[ChargeType] = ChargeType.ON_NET_TOTAL

    row_id: Optional[str] = None

    allocate_full_amount_to_stock_items: Optional[bool] = True

    included_in_print_rate: Optional[bool] = False

    account_head_id: uuid.UUID

    cost_center_id: Optional[uuid.UUID] = None

    description: str

    rate: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    tax_amount_after_discount_amount: Optional[Decimal] = None

    total: Optional[Decimal] = None

    base_tax_amount: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_tax_amount_after_discount_amount: Optional[Decimal] = None

    project: Optional[str] = None

    included_in_paid_amount: Optional[bool] = False

    account_currency: Optional[str] = None

    net_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    is_tax_withholding_account: Optional[bool] = False

    set_by_item_tax_template: Optional[bool] = False

    dont_recompute_tax: Optional[bool] = False





class PurchaseTaxesAndChargesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    category: Optional[PurchaseTaxCategory] = None

    add_deduct_tax: Optional[AddDeductTax] = None

    charge_type: Optional[ChargeType] = None

    row_id: Optional[str] = None

    allocate_full_amount_to_stock_items: bool

    included_in_print_rate: bool

    account_head_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    rate: Optional[Decimal] = None

    tax_amount: Optional[Decimal] = None

    tax_amount_after_discount_amount: Optional[Decimal] = None

    total: Optional[Decimal] = None

    base_tax_amount: Optional[Decimal] = None

    base_total: Optional[Decimal] = None

    base_tax_amount_after_discount_amount: Optional[Decimal] = None

    project: Optional[str] = None

    included_in_paid_amount: bool

    account_currency: Optional[str] = None

    net_amount: Optional[Decimal] = None

    base_net_amount: Optional[Decimal] = None

    is_tax_withholding_account: bool

    set_by_item_tax_template: bool

    dont_recompute_tax: bool





PurchaseTaxesAndChargesListResponse = Page[PurchaseTaxesAndChargesRead]
