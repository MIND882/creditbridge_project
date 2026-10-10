"""

Pricing Rule -- converted from ``erpnext/accounts/doctype/pricing_rule``.





"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pricing_rule_brand_domain.models.pricing_rule_brand import PricingRuleBrand

from app.accounts.pricing_rule_item_code_domain.models.pricing_rule_item_code import PricingRuleItemCode

from app.accounts.pricing_rule_item_group_domain.models.pricing_rule_item_group import PricingRuleItemGroup



from app.core.base_model import TenantModel



__all__ = ["PricingRule", "PricingRuleApplyOn", "PricingRulePriceOrProductDiscount", "PricingRuleApplyRuleOnOther", "PricingRuleApplicableFor", "PricingRuleMarginType", "PricingRuleRateOrDiscount", "PricingRuleApplyDiscountOn", "PricingRulePriority", "PricingRuleNamingSeries"]







class PricingRuleApplyOn(str, enum.Enum):

    ITEM_CODE = "Item Code"

    ITEM_GROUP = "Item Group"

    BRAND = "Brand"

    TRANSACTION = "Transaction"





class PricingRulePriceOrProductDiscount(str, enum.Enum):

    PRICE = "Price"

    PRODUCT = "Product"





class PricingRuleApplyRuleOnOther(str, enum.Enum):

    ITEM_CODE = "Item Code"

    ITEM_GROUP = "Item Group"

    BRAND = "Brand"





class PricingRuleApplicableFor(str, enum.Enum):

    CUSTOMER = "Customer"

    CUSTOMER_GROUP = "Customer Group"

    TERRITORY = "Territory"

    SALES_PARTNER = "Sales Partner"

    CAMPAIGN = "Campaign"

    SUPPLIER = "Supplier"

    SUPPLIER_GROUP = "Supplier Group"





class PricingRuleMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class PricingRuleRateOrDiscount(str, enum.Enum):

    RATE = "Rate"

    DISCOUNT_PERCENTAGE = "Discount Percentage"

    DISCOUNT_AMOUNT = "Discount Amount"





class PricingRuleApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"





class PricingRulePriority(str, enum.Enum):

    _1 = "1"

    _2 = "2"

    _3 = "3"

    _4 = "4"

    _5 = "5"

    _6 = "6"

    _7 = "7"

    _8 = "8"

    _9 = "9"

    _10 = "10"

    _11 = "11"

    _12 = "12"

    _13 = "13"

    _14 = "14"

    _15 = "15"

    _16 = "16"

    _17 = "17"

    _18 = "18"

    _19 = "19"

    _20 = "20"





class PricingRuleNamingSeries(str, enum.Enum):

    PRLE = "PRLE-.####"









class PricingRule(TenantModel):

    __tablename__ = "pricing_rules"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pricing_rules_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    title: Mapped[str] = mapped_column(String(140), nullable=False)

    disable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_on: Mapped[PricingRuleApplyOn] = mapped_column(

        SAEnum(PricingRuleApplyOn, native_enum=False, length=11, validate_strings=True),

        nullable=False,

    )

    price_or_product_discount: Mapped[PricingRulePriceOrProductDiscount] = mapped_column(

        SAEnum(PricingRulePriceOrProductDiscount, native_enum=False, length=7, validate_strings=True),

        nullable=False,

    )

    warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mixed_conditions: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_cumulative: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    coupon_code_based: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_rule_on_other: Mapped[Optional[PricingRuleApplyRuleOnOther]] = mapped_column(

        SAEnum(PricingRuleApplyRuleOnOther, native_enum=False, length=10, validate_strings=True),

        nullable=True,

    )

    other_item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    other_item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    other_brand: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    selling: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    buying: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    applicable_for: Mapped[Optional[PricingRuleApplicableFor]] = mapped_column(

        SAEnum(PricingRuleApplicableFor, native_enum=False, length=14, validate_strings=True),

        nullable=True,

    )

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    min_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    min_amt: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_amt: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valid_from: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    valid_upto: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    margin_type: Mapped[Optional[PricingRuleMarginType]] = mapped_column(

        SAEnum(PricingRuleMarginType, native_enum=False, length=10, validate_strings=True),

        nullable=True,

    )

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_or_discount: Mapped[Optional[PricingRuleRateOrDiscount]] = mapped_column(

        SAEnum(PricingRuleRateOrDiscount, native_enum=False, length=19, validate_strings=True),

        nullable=True,

    )

    apply_discount_on: Mapped[Optional[PricingRuleApplyDiscountOn]] = mapped_column(

        SAEnum(PricingRuleApplyDiscountOn, native_enum=False, length=11, validate_strings=True),

        nullable=True,

    )

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    for_price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    same_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    free_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    free_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    free_item_uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    free_item_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    threshold_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    priority: Mapped[Optional[PricingRulePriority]] = mapped_column(

        SAEnum(PricingRulePriority, native_enum=False, length=3, validate_strings=True),

        nullable=True,

    )

    apply_multiple_pricing_rules: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_discount_on_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    validate_applied_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    rule_description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    promotional_scheme_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    promotional_scheme: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_recursive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    naming_series: Mapped[Optional[PricingRuleNamingSeries]] = mapped_column(

        SAEnum(PricingRuleNamingSeries, native_enum=False, length=10, validate_strings=True),

        nullable=True,

    )

    round_free_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    recurse_for: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_recursion_over: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    has_priority: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    dont_enforce_free_item_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    items = relationship(

        PricingRuleItemCode,

        primaryjoin="and_(PricingRule.id == foreign(PricingRuleItemCode.parent_id), PricingRuleItemCode.parenttype == 'Pricing Rule')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleItemCode.idx,

        overlaps="items",

    )

    item_groups = relationship(

        PricingRuleItemGroup,

        primaryjoin="and_(PricingRule.id == foreign(PricingRuleItemGroup.parent_id), PricingRuleItemGroup.parenttype == 'Pricing Rule')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleItemGroup.idx,

        overlaps="item_groups",

    )

    brands = relationship(

        PricingRuleBrand,

        primaryjoin="and_(PricingRule.id == foreign(PricingRuleBrand.parent_id), PricingRuleBrand.parenttype == 'Pricing Rule')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleBrand.idx,

        overlaps="brands",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PricingRule id={self.id}>"
