"""Pydantic v2 schemas for PromotionalScheme."""





from __future__ import annotations

from app.accounts.promotional_scheme_domain.models.promotional_scheme import (

    PromotionalSchemeApplicableFor,

    PromotionalSchemeApplyOn,

    PromotionalSchemeApplyRuleOnOther,

)

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

from app.accounts.customer_item_domain.schemas.customer_item import (

    CustomerItemCreate,

    CustomerItemRead,

)

from app.accounts.customer_group_item_domain.schemas.customer_group_item import (

    CustomerGroupItemCreate,

    CustomerGroupItemRead,

)

from app.accounts.territory_item_domain.schemas.territory_item import (

    TerritoryItemCreate,

    TerritoryItemRead,

)

from app.accounts.sales_partner_item_domain.schemas.sales_partner_item import (

    SalesPartnerItemCreate,

    SalesPartnerItemRead,

)

from app.accounts.campaign_item_domain.schemas.campaign_item import (

    CampaignItemCreate,

    CampaignItemRead,

)

from app.accounts.supplier_item_domain.schemas.supplier_item import (

    SupplierItemCreate,

    SupplierItemRead,

)

from app.accounts.supplier_group_item_domain.schemas.supplier_group_item import (

    SupplierGroupItemCreate,

    SupplierGroupItemRead,

)

from app.accounts.promotional_scheme_price_discount_domain.schemas.promotional_scheme_price_discount import (

    PromotionalSchemePriceDiscountCreate,

    PromotionalSchemePriceDiscountRead,

)

from app.accounts.promotional_scheme_product_discount_domain.schemas.promotional_scheme_product_discount import (

    PromotionalSchemeProductDiscountCreate,

    PromotionalSchemeProductDiscountRead,

)



__all__ = [

    "PromotionalSchemeCreate",

    "PromotionalSchemeUpdate",

    "PromotionalSchemeRead",

    "PromotionalSchemeListResponse",

]





class PromotionalSchemeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    apply_on: PromotionalSchemeApplyOn

    disable: Optional[bool] = None

    mixed_conditions: Optional[bool] = None

    is_cumulative: Optional[bool] = None

    apply_rule_on_other: Optional[PromotionalSchemeApplyRuleOnOther] = None

    other_item_code: Optional[str] = None

    other_item_group: Optional[str] = None

    other_brand: Optional[str] = None

    selling: Optional[bool] = None

    buying: Optional[bool] = None

    applicable_for: Optional[PromotionalSchemeApplicableFor] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    currency: Optional[str] = None



    items: list[PricingRuleItemCodeCreate] = []



    item_groups: list[PricingRuleItemGroupCreate] = []



    brands: list[PricingRuleBrandCreate] = []



    customer: list[CustomerItemCreate] = []



    customer_group: list[CustomerGroupItemCreate] = []



    territory: list[TerritoryItemCreate] = []



    sales_partner: list[SalesPartnerItemCreate] = []



    campaign: list[CampaignItemCreate] = []



    supplier: list[SupplierItemCreate] = []



    supplier_group: list[SupplierGroupItemCreate] = []



    price_discount_slabs: list[PromotionalSchemePriceDiscountCreate] = []



    product_discount_slabs: list[PromotionalSchemeProductDiscountCreate] = []





class PromotionalSchemeCreate(PromotionalSchemeBase):

    pass





class PromotionalSchemeUpdate(InputSchema):

    """A partial update."""



    apply_on: Optional[PromotionalSchemeApplyOn] = None

    disable: Optional[bool] = None

    mixed_conditions: Optional[bool] = None

    is_cumulative: Optional[bool] = None

    apply_rule_on_other: Optional[PromotionalSchemeApplyRuleOnOther] = None

    other_item_code: Optional[str] = None

    other_item_group: Optional[str] = None

    other_brand: Optional[str] = None

    selling: Optional[bool] = None

    buying: Optional[bool] = None

    applicable_for: Optional[PromotionalSchemeApplicableFor] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    currency: Optional[str] = None

    items: Optional[list[PricingRuleItemCodeCreate]] = None

    item_groups: Optional[list[PricingRuleItemGroupCreate]] = None

    brands: Optional[list[PricingRuleBrandCreate]] = None

    customer: Optional[list[CustomerItemCreate]] = None

    customer_group: Optional[list[CustomerGroupItemCreate]] = None

    territory: Optional[list[TerritoryItemCreate]] = None

    sales_partner: Optional[list[SalesPartnerItemCreate]] = None

    campaign: Optional[list[CampaignItemCreate]] = None

    supplier: Optional[list[SupplierItemCreate]] = None

    supplier_group: Optional[list[SupplierGroupItemCreate]] = None

    price_discount_slabs: Optional[list[PromotionalSchemePriceDiscountCreate]] = None

    product_discount_slabs: Optional[list[PromotionalSchemeProductDiscountCreate]] = None





class PromotionalSchemeRead(ReadSchema):

    id: uuid.UUID

    name: str

    apply_on: PromotionalSchemeApplyOn

    disable: bool

    mixed_conditions: bool

    is_cumulative: bool

    apply_rule_on_other: Optional[PromotionalSchemeApplyRuleOnOther] = None

    other_item_code: Optional[str] = None

    other_item_group: Optional[str] = None

    other_brand: Optional[str] = None

    selling: bool

    buying: bool

    applicable_for: Optional[PromotionalSchemeApplicableFor] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    currency: Optional[str] = None

    items: list[PricingRuleItemCodeRead] = []

    item_groups: list[PricingRuleItemGroupRead] = []

    brands: list[PricingRuleBrandRead] = []

    customer: list[CustomerItemRead] = []

    customer_group: list[CustomerGroupItemRead] = []

    territory: list[TerritoryItemRead] = []

    sales_partner: list[SalesPartnerItemRead] = []

    campaign: list[CampaignItemRead] = []

    supplier: list[SupplierItemRead] = []

    supplier_group: list[SupplierGroupItemRead] = []

    price_discount_slabs: list[PromotionalSchemePriceDiscountRead] = []

    product_discount_slabs: list[PromotionalSchemeProductDiscountRead] = []





PromotionalSchemeListResponse = Page[PromotionalSchemeRead]
