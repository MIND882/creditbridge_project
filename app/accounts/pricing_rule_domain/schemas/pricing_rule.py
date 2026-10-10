"""Pydantic v2 schemas for PricingRule."""





from __future__ import annotations

from app.accounts.pricing_rule_domain.models.pricing_rule import (

    PricingRuleApplicableFor,

    PricingRuleApplyDiscountOn,

    PricingRuleApplyOn,

    PricingRuleApplyRuleOnOther,

    PricingRuleMarginType,

    PricingRuleNamingSeries,

    PricingRulePriceOrProductDiscount,

    PricingRulePriority,

    PricingRuleRateOrDiscount,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.accounts.pricing_rule_item_code_domain.schemas.pricing_rule_item_code import (

    PricingRuleItemCodeCreate,

    PricingRuleItemCodeRead,

)

from app.accounts.pricing_rule_item_group_domain.schemas.pricing_rule_item_group import (

    PricingRuleItemGroupCreate,

    PricingRuleItemGroupRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_invoice_item_domain.schemas.pos_invoice_item import (

    POSInvoiceItemCreate,

    POSInvoiceItemRead,

)

from app.accounts.pos_item_group_domain.schemas.pos_item_group import (

    POSItemGroupCreate,

    POSItemGroupRead,

)

from app.accounts.pricing_rule_brand_domain.schemas.pricing_rule_brand import (

    PricingRuleBrandCreate,

    PricingRuleBrandRead,

)



__all__ = [

    "PricingRuleCreate",

    "PricingRuleUpdate",

    "PricingRuleRead",

    "PricingRuleListResponse",

]





class PricingRuleBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    title: str

    disable: Optional[bool] = None

    apply_on: PricingRuleApplyOn

    price_or_product_discount: PricingRulePriceOrProductDiscount

    warehouse: Optional[str] = None

    mixed_conditions: Optional[bool] = None

    is_cumulative: Optional[bool] = None

    coupon_code_based: Optional[bool] = None

    apply_rule_on_other: Optional[PricingRuleApplyRuleOnOther] = None

    other_item_code: Optional[str] = None

    other_item_group: Optional[str] = None

    other_brand: Optional[str] = None

    selling: Optional[bool] = None

    buying: Optional[bool] = None

    applicable_for: Optional[PricingRuleApplicableFor] = None

    customer: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    sales_partner: Optional[str] = None

    campaign: Optional[str] = None

    supplier: Optional[str] = None

    supplier_group: Optional[str] = None

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amt: Optional[Decimal] = None

    max_amt: Optional[Decimal] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    currency: str

    margin_type: Optional[PricingRuleMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_or_discount: Optional[PricingRuleRateOrDiscount] = None

    apply_discount_on: Optional[PricingRuleApplyDiscountOn] = None

    rate: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    for_price_list: Optional[str] = None

    same_item: Optional[bool] = None

    free_item: Optional[str] = None

    free_qty: Optional[Decimal] = None

    free_item_uom: Optional[str] = None

    free_item_rate: Optional[Decimal] = None

    threshold_percentage: Optional[Decimal] = None

    priority: Optional[PricingRulePriority] = None

    apply_multiple_pricing_rules: Optional[bool] = None

    apply_discount_on_rate: Optional[bool] = None

    validate_applied_rule: Optional[bool] = None

    rule_description: Optional[str] = None

    promotional_scheme: Optional[str] = None

    condition: Optional[str] = None

    is_recursive: Optional[bool] = None

    naming_series: Optional[PricingRuleNamingSeries] = None

    round_free_qty: Optional[bool] = None

    recurse_for: Optional[Decimal] = None

    apply_recursion_over: Optional[Decimal] = None

    has_priority: Optional[bool] = None

    dont_enforce_free_item_qty: Optional[bool] = None



    items: list[PricingRuleItemCodeCreate] = []



    item_groups: list[PricingRuleItemGroupCreate] = []



    brands: list[PricingRuleBrandCreate] = []





class PricingRuleCreate(PricingRuleBase):

    pass





class PricingRuleUpdate(InputSchema):

    """A partial update."""



    title: Optional[str] = None

    disable: Optional[bool] = None

    apply_on: Optional[PricingRuleApplyOn] = None

    price_or_product_discount: Optional[PricingRulePriceOrProductDiscount] = None

    warehouse: Optional[str] = None

    mixed_conditions: Optional[bool] = None

    is_cumulative: Optional[bool] = None

    coupon_code_based: Optional[bool] = None

    apply_rule_on_other: Optional[PricingRuleApplyRuleOnOther] = None

    other_item_code: Optional[str] = None

    other_item_group: Optional[str] = None

    other_brand: Optional[str] = None

    selling: Optional[bool] = None

    buying: Optional[bool] = None

    applicable_for: Optional[PricingRuleApplicableFor] = None

    customer: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    sales_partner: Optional[str] = None

    campaign: Optional[str] = None

    supplier: Optional[str] = None

    supplier_group: Optional[str] = None

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amt: Optional[Decimal] = None

    max_amt: Optional[Decimal] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    currency: Optional[str] = None

    margin_type: Optional[PricingRuleMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_or_discount: Optional[PricingRuleRateOrDiscount] = None

    apply_discount_on: Optional[PricingRuleApplyDiscountOn] = None

    rate: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    for_price_list: Optional[str] = None

    same_item: Optional[bool] = None

    free_item: Optional[str] = None

    free_qty: Optional[Decimal] = None

    free_item_uom: Optional[str] = None

    free_item_rate: Optional[Decimal] = None

    threshold_percentage: Optional[Decimal] = None

    priority: Optional[PricingRulePriority] = None

    apply_multiple_pricing_rules: Optional[bool] = None

    apply_discount_on_rate: Optional[bool] = None

    validate_applied_rule: Optional[bool] = None

    rule_description: Optional[str] = None

    promotional_scheme: Optional[str] = None

    condition: Optional[str] = None

    is_recursive: Optional[bool] = None

    naming_series: Optional[PricingRuleNamingSeries] = None

    round_free_qty: Optional[bool] = None

    recurse_for: Optional[Decimal] = None

    apply_recursion_over: Optional[Decimal] = None

    has_priority: Optional[bool] = None

    dont_enforce_free_item_qty: Optional[bool] = None

    items: Optional[list[PricingRuleItemCodeCreate]] = None

    item_groups: Optional[list[PricingRuleItemGroupCreate]] = None

    brands: Optional[list[PricingRuleBrandCreate]] = None





class PricingRuleRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: str

    disable: bool

    apply_on: PricingRuleApplyOn

    price_or_product_discount: PricingRulePriceOrProductDiscount

    warehouse: Optional[str] = None

    mixed_conditions: bool

    is_cumulative: bool

    coupon_code_based: bool

    apply_rule_on_other: Optional[PricingRuleApplyRuleOnOther] = None

    other_item_code: Optional[str] = None

    other_item_group: Optional[str] = None

    other_brand: Optional[str] = None

    selling: bool

    buying: bool

    applicable_for: Optional[PricingRuleApplicableFor] = None

    customer: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    sales_partner: Optional[str] = None

    campaign: Optional[str] = None

    supplier: Optional[str] = None

    supplier_group: Optional[str] = None

    min_qty: Optional[Decimal] = None

    max_qty: Optional[Decimal] = None

    min_amt: Optional[Decimal] = None

    max_amt: Optional[Decimal] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    currency: str

    margin_type: Optional[PricingRuleMarginType] = None

    margin_rate_or_amount: Optional[Decimal] = None

    rate_or_discount: Optional[PricingRuleRateOrDiscount] = None

    apply_discount_on: Optional[PricingRuleApplyDiscountOn] = None

    rate: Optional[Decimal] = None

    discount_amount: Optional[Decimal] = None

    discount_percentage: Optional[Decimal] = None

    for_price_list: Optional[str] = None

    same_item: bool

    free_item: Optional[str] = None

    free_qty: Optional[Decimal] = None

    free_item_uom: Optional[str] = None

    free_item_rate: Optional[Decimal] = None

    threshold_percentage: Optional[Decimal] = None

    priority: Optional[PricingRulePriority] = None

    apply_multiple_pricing_rules: bool

    apply_discount_on_rate: bool

    validate_applied_rule: bool

    rule_description: Optional[str] = None

    promotional_scheme: Optional[str] = None

    condition: Optional[str] = None

    is_recursive: bool

    naming_series: Optional[PricingRuleNamingSeries] = None

    round_free_qty: bool

    recurse_for: Optional[Decimal] = None

    apply_recursion_over: Optional[Decimal] = None

    has_priority: bool

    dont_enforce_free_item_qty: bool

    items: list[PricingRuleItemCodeRead] = []

    item_groups: list[PricingRuleItemGroupRead] = []

    brands: list[PricingRuleBrandRead] = []





PricingRuleListResponse = Page[PricingRuleRead]
