"""

Promotional Scheme -- converted from ``erpnext/accounts/doctype/promotional_scheme``.





"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.campaign_item_domain.models.campaign_item import CampaignItem

from app.accounts.customer_group_item_domain.models.customer_group_item import CustomerGroupItem

from app.accounts.customer_item_domain.models.customer_item import CustomerItem

from app.accounts.pricing_rule_brand_domain.models.pricing_rule_brand import PricingRuleBrand

from app.accounts.pricing_rule_item_code_domain.models.pricing_rule_item_code import PricingRuleItemCode

from app.accounts.pricing_rule_item_group_domain.models.pricing_rule_item_group import PricingRuleItemGroup

from app.accounts.promotional_scheme_price_discount_domain.models.promotional_scheme_price_discount import PromotionalSchemePriceDiscount

from app.accounts.promotional_scheme_product_discount_domain.models.promotional_scheme_product_discount import PromotionalSchemeProductDiscount

from app.accounts.sales_partner_item_domain.models.sales_partner_item import SalesPartnerItem

from app.accounts.supplier_group_item_domain.models.supplier_group_item import SupplierGroupItem

from app.accounts.supplier_item_domain.models.supplier_item import SupplierItem

from app.accounts.territory_item_domain.models.territory_item import TerritoryItem



from app.core.base_model import TenantModel



__all__ = ["PromotionalScheme", "PromotionalSchemeApplyOn", "PromotionalSchemeApplyRuleOnOther", "PromotionalSchemeApplicableFor"]







class PromotionalSchemeApplyOn(str, enum.Enum):

    ITEM_CODE = "Item Code"

    ITEM_GROUP = "Item Group"

    BRAND = "Brand"

    TRANSACTION = "Transaction"





class PromotionalSchemeApplyRuleOnOther(str, enum.Enum):

    ITEM_CODE = "Item Code"

    ITEM_GROUP = "Item Group"

    BRAND = "Brand"





class PromotionalSchemeApplicableFor(str, enum.Enum):

    CUSTOMER = "Customer"

    CUSTOMER_GROUP = "Customer Group"

    TERRITORY = "Territory"

    SALES_PARTNER = "Sales Partner"

    CAMPAIGN = "Campaign"

    SUPPLIER = "Supplier"

    SUPPLIER_GROUP = "Supplier Group"









class PromotionalScheme(TenantModel):

    __tablename__ = "promotional_schemes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_promotional_schemes_business_name"),

    )



    #: ``autoname`` = 'Prompt'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    apply_on: Mapped[PromotionalSchemeApplyOn] = mapped_column(

        SAEnum(PromotionalSchemeApplyOn, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    disable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    mixed_conditions: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_cumulative: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_rule_on_other: Mapped[Optional[PromotionalSchemeApplyRuleOnOther]] = mapped_column(

        SAEnum(PromotionalSchemeApplyRuleOnOther, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    other_item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    other_item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    other_brand: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    selling: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    buying: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    applicable_for: Mapped[Optional[PromotionalSchemeApplicableFor]] = mapped_column(

        SAEnum(PromotionalSchemeApplicableFor, native_enum=False, length=14, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    valid_from: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    valid_upto: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items = relationship(

        PricingRuleItemCode,

        primaryjoin="and_(PromotionalScheme.id == foreign(PricingRuleItemCode.parent_id), PricingRuleItemCode.parenttype == 'Promotional Scheme')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleItemCode.idx,

        overlaps="items",

    )

    item_groups = relationship(

        PricingRuleItemGroup,

        primaryjoin="and_(PromotionalScheme.id == foreign(PricingRuleItemGroup.parent_id), PricingRuleItemGroup.parenttype == 'Promotional Scheme')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleItemGroup.idx,

        overlaps="item_groups",

    )

    brands = relationship(

        PricingRuleBrand,

        primaryjoin="and_(PromotionalScheme.id == foreign(PricingRuleBrand.parent_id), PricingRuleBrand.parenttype == 'Promotional Scheme')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=PricingRuleBrand.idx,

        overlaps="brands",

    )

    customer = relationship(

        CustomerItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=CustomerItem.idx,

        passive_deletes=True,

    )

    customer_group = relationship(

        CustomerGroupItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=CustomerGroupItem.idx,

        passive_deletes=True,

    )

    territory = relationship(

        TerritoryItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=TerritoryItem.idx,

        passive_deletes=True,

    )

    sales_partner = relationship(

        SalesPartnerItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=SalesPartnerItem.idx,

        passive_deletes=True,

    )

    campaign = relationship(

        CampaignItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=CampaignItem.idx,

        passive_deletes=True,

    )

    supplier = relationship(

        SupplierItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=SupplierItem.idx,

        passive_deletes=True,

    )

    supplier_group = relationship(

        SupplierGroupItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=SupplierGroupItem.idx,

        passive_deletes=True,

    )

    price_discount_slabs = relationship(

        PromotionalSchemePriceDiscount,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PromotionalSchemePriceDiscount.idx,

        passive_deletes=True,

    )

    product_discount_slabs = relationship(

        PromotionalSchemeProductDiscount,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PromotionalSchemeProductDiscount.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PromotionalScheme id={self.id}>"
