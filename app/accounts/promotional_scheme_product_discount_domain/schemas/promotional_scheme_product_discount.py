"""Pydantic v2 schemas for PromotionalSchemeProductDiscount."""





from __future__ import annotations

from app.accounts.promotional_scheme_product_discount_domain.models.promotional_scheme_product_discount import (

    PromotionalSchemeProductDiscountPriority,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PromotionalSchemeProductDiscountCreate",

    "PromotionalSchemeProductDiscountRead",

    "PromotionalSchemeProductDiscountListResponse",

]





class PromotionalSchemeProductDiscountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    disable: Optional[bool] = None

    rule_description: str

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amount: Optional[Decimal] = None

    max_amount: Optional[Decimal] = None

    same_item: Optional[bool] = None

    free_item: Optional[str] = None

    free_qty: Optional[Decimal] = None

    free_item_uom: Optional[str] = None

    free_item_rate: Optional[Decimal] = None

    warehouse: Optional[str] = None

    threshold_percentage: Optional[Decimal] = None

    priority: Optional[PromotionalSchemeProductDiscountPriority] = None

    apply_multiple_pricing_rules: Optional[bool] = None

    is_recursive: Optional[bool] = None

    recurse_for: Optional[Decimal] = None

    apply_recursion_over: Optional[Decimal] = None

    round_free_qty: Optional[bool] = None





class PromotionalSchemeProductDiscountCreate(PromotionalSchemeProductDiscountBase):

    """Accepted only nested inside the parent payload."""

    pass





class PromotionalSchemeProductDiscountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    disable: bool

    rule_description: str

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amount: Optional[Decimal] = None

    max_amount: Optional[Decimal] = None

    same_item: bool

    free_item: Optional[str] = None

    free_qty: Optional[Decimal] = None

    free_item_uom: Optional[str] = None

    free_item_rate: Optional[Decimal] = None

    warehouse: Optional[str] = None

    threshold_percentage: Optional[Decimal] = None

    priority: Optional[PromotionalSchemeProductDiscountPriority] = None

    apply_multiple_pricing_rules: bool

    is_recursive: bool

    recurse_for: Optional[Decimal] = None

    apply_recursion_over: Optional[Decimal] = None

    round_free_qty: bool





PromotionalSchemeProductDiscountListResponse = Page[PromotionalSchemeProductDiscountRead]
