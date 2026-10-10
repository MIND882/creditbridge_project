"""Pydantic v2 schemas for PromotionalSchemePriceDiscount."""





from __future__ import annotations

from app.accounts.promotional_scheme_price_discount_domain.models.promotional_scheme_price_discount import (

    PromotionalSchemePriceDiscountPriority,

    PromotionalSchemePriceDiscountRateOrDiscount,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PromotionalSchemePriceDiscountCreate",

    "PromotionalSchemePriceDiscountRead",

    "PromotionalSchemePriceDiscountListResponse",

]





class PromotionalSchemePriceDiscountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    disable: Optional[bool] = None

    rule_description: str

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amount: Optional[Decimal] = None

    max_amount: Optional[Decimal] = None

    rate_or_discount: Optional[PromotionalSchemePriceDiscountRateOrDiscount] = None

    rate: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    for_price_list: Optional[str] = None

    warehouse: Optional[str] = None

    threshold_percentage: Optional[Decimal] = None

    validate_applied_rule: Optional[bool] = None

    priority: Optional[PromotionalSchemePriceDiscountPriority] = None

    apply_multiple_pricing_rules: Optional[bool] = None

    apply_discount_on_rate: Optional[bool] = None





class PromotionalSchemePriceDiscountCreate(PromotionalSchemePriceDiscountBase):

    """Accepted only nested inside the parent payload."""

    pass





class PromotionalSchemePriceDiscountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    disable: bool

    rule_description: str

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amount: Optional[Decimal] = None

    max_amount: Optional[Decimal] = None

    rate_or_discount: Optional[PromotionalSchemePriceDiscountRateOrDiscount] = None

    rate: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    for_price_list: Optional[str] = None

    warehouse: Optional[str] = None

    threshold_percentage: Optional[Decimal] = None

    validate_applied_rule: bool

    priority: Optional[PromotionalSchemePriceDiscountPriority] = None

    apply_multiple_pricing_rules: bool

    apply_discount_on_rate: bool





PromotionalSchemePriceDiscountListResponse = Page[PromotionalSchemePriceDiscountRead]
