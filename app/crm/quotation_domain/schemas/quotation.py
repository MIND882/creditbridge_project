# app/crm/quotation_domain/schemas/quotation.py

"""
Pydantic schemas for the Quotation domain — full field parity, matching
the expanded SQLAlchemy model (main table + Items/Taxes/PaymentSchedule
child tables).
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class QuotationStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_ORDERED = "partially_ordered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class QuotationOrderType(str, Enum):
    SALES = "sales"
    MAINTENANCE = "maintenance"
    SHOPPING_CART = "shopping_cart"


# ── Child: Item ───────────────────────────────────────────────────────────
class QuotationItemPayload(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    qty: Decimal = Field(1, gt=0)
    uom: Optional[str] = Field(None, max_length=50)
    rate: Decimal = Field(0, ge=0)
    is_alternative: bool = False
    is_free_item: bool = False


class QuotationItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    item_name: str
    description: Optional[str]
    qty: Decimal
    uom: Optional[str]
    rate: Decimal
    amount: Decimal
    is_alternative: bool
    is_free_item: bool
    idx: int


# ── Child: Tax ────────────────────────────────────────────────────────────
class QuotationTaxPayload(BaseModel):
    charge_type: str = Field("On Net Total", max_length=30)
    description: str = Field(..., min_length=1, max_length=255)
    rate: Optional[Decimal] = Field(None, ge=0, le=100)
    tax_amount: Decimal = Field(0, ge=0)


class QuotationTaxResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    charge_type: str
    description: str
    rate: Optional[Decimal]
    tax_amount: Decimal
    total: Decimal
    idx: int


# ── Child: Payment Schedule Entry ───────────────────────────────────────────
class QuotationPaymentScheduleEntryPayload(BaseModel):
    description: Optional[str] = Field(None, max_length=255)
    due_date: date
    invoice_portion_percent: Optional[Decimal] = Field(None, ge=0, le=100)
    payment_amount: Decimal = Field(0, ge=0)


class QuotationPaymentScheduleEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    description: Optional[str]
    due_date: date
    invoice_portion_percent: Optional[Decimal]
    payment_amount: Decimal
    idx: int


# ── Create payload ───────────────────────────────────────────────────────────
class QuotationCreatePayload(BaseModel):
    opportunity_id: uuid.UUID
    title: Optional[str] = Field(None, max_length=255)
    transaction_date: Optional[date] = None
    valid_till: Optional[date] = None
    order_type: QuotationOrderType = QuotationOrderType.SALES
    has_unit_price_items: bool = False

    currency: str = Field("INR", min_length=3, max_length=3)
    conversion_rate: Decimal = Field(1, gt=0)
    selling_price_list: Optional[str] = Field(None, max_length=100)
    price_list_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    plc_conversion_rate: Decimal = Field(1, gt=0)
    ignore_pricing_rule: bool = False
    pricing_rules: Optional[list[str]] = None

    tax_category: Optional[str] = Field(None, max_length=100)
    taxes_and_charges_template: Optional[str] = Field(None, max_length=255)

    shipping_rule: Optional[str] = Field(None, max_length=100)
    incoterm: Optional[str] = Field(None, max_length=10)
    named_place: Optional[str] = Field(None, max_length=255)

    apply_discount_on: Optional[str] = Field(None, max_length=20)
    additional_discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    coupon_code: Optional[str] = Field(None, max_length=50)
    referral_sales_partner: Optional[str] = Field(None, max_length=255)

    payment_terms_template: Optional[str] = Field(None, max_length=255)
    payment_due_date: Optional[date] = None
    payment_amount: Optional[Decimal] = Field(None, ge=0)

    tc_name: Optional[str] = Field(None, max_length=255)
    terms: Optional[str] = None

    letter_head: Optional[str] = Field(None, max_length=255)
    group_same_items: bool = False
    select_print_heading: Optional[str] = Field(None, max_length=255)
    language: Optional[str] = Field(None, max_length=20)

    customer_address: Optional[str] = None
    shipping_address: Optional[str] = None
    company_address: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=255)
    contact_mobile: Optional[str] = Field(None, max_length=15)
    contact_email: Optional[EmailStr] = None

    utm_source: Optional[str] = Field(None, max_length=100)
    utm_medium: Optional[str] = Field(None, max_length=100)
    utm_campaign: Optional[str] = Field(None, max_length=100)
    utm_content: Optional[str] = Field(None, max_length=100)

    scan_barcode: Optional[str] = Field(None, max_length=100)
    customer_group: Optional[str] = Field(None, max_length=100)
    territory: Optional[str] = Field(None, max_length=100)

    items: list[QuotationItemPayload] = Field(default_factory=list)
    taxes: list[QuotationTaxPayload] = Field(default_factory=list)
    payment_schedule_entries: list[QuotationPaymentScheduleEntryPayload] = Field(default_factory=list)


# ── Update payload ───────────────────────────────────────────────────────────
class QuotationUpdatePayload(BaseModel):
    """
    Partial update. `opportunity_id` intentionally NOT editable. Passing
    `items` / `taxes` / `payment_schedule_entries` REPLACES the full set
    for that quotation (not a merge) — matches ERPNext's grid-edit
    semantics where the whole child table is resaved on each update.
    """

    title: Optional[str] = Field(None, max_length=255)
    valid_till: Optional[date] = None
    has_unit_price_items: Optional[bool] = None

    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    conversion_rate: Optional[Decimal] = Field(None, gt=0)
    selling_price_list: Optional[str] = Field(None, max_length=100)
    ignore_pricing_rule: Optional[bool] = None
    pricing_rules: Optional[list[str]] = None

    tax_category: Optional[str] = Field(None, max_length=100)
    taxes_and_charges_template: Optional[str] = Field(None, max_length=255)

    shipping_rule: Optional[str] = Field(None, max_length=100)
    incoterm: Optional[str] = Field(None, max_length=10)
    named_place: Optional[str] = Field(None, max_length=255)

    apply_discount_on: Optional[str] = Field(None, max_length=20)
    additional_discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    coupon_code: Optional[str] = Field(None, max_length=50)

    payment_terms_template: Optional[str] = Field(None, max_length=255)
    payment_due_date: Optional[date] = None
    payment_amount: Optional[Decimal] = Field(None, ge=0)

    terms: Optional[str] = None
    letter_head: Optional[str] = Field(None, max_length=255)

    items: Optional[list[QuotationItemPayload]] = None
    taxes: Optional[list[QuotationTaxPayload]] = None
    payment_schedule_entries: Optional[list[QuotationPaymentScheduleEntryPayload]] = None


# ── Reject payload ───────────────────────────────────────────────────────────
class QuotationRejectPayload(BaseModel):
    rejection_reason: str = Field(..., min_length=1)
    lost_reasons: Optional[list[str]] = None
    competitors: Optional[list[str]] = None


# ── Accept payload ───────────────────────────────────────────────────────────
class QuotationAcceptPayload(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(None, max_length=15)


# ── Response schemas ─────────────────────────────────────────────────────────
class QuotationListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    opportunity_id: uuid.UUID
    title: Optional[str]
    transaction_date: date
    currency: str
    grand_total: Optional[Decimal]
    status: QuotationStatus
    valid_till: Optional[date]
    created_at: datetime


class QuotationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    opportunity_id: uuid.UUID
    converted_customer_id: Optional[uuid.UUID]

    title: Optional[str]
    transaction_date: date
    valid_till: Optional[date]
    order_type: QuotationOrderType
    has_unit_price_items: bool

    currency: str
    conversion_rate: Decimal
    selling_price_list: Optional[str]
    price_list_currency: Optional[str]
    plc_conversion_rate: Decimal
    ignore_pricing_rule: bool
    pricing_rules: Optional[list[str]]

    total_qty: Optional[Decimal]
    total_net_weight: Optional[Decimal]
    base_total: Optional[Decimal]
    base_net_total: Optional[Decimal]
    total: Optional[Decimal]
    net_total: Optional[Decimal]

    tax_category: Optional[str]
    taxes_and_charges_template: Optional[str]
    base_total_taxes_and_charges: Optional[Decimal]
    total_taxes_and_charges: Optional[Decimal]

    shipping_rule: Optional[str]
    incoterm: Optional[str]
    named_place: Optional[str]

    apply_discount_on: Optional[str]
    base_discount_amount: Optional[Decimal]
    additional_discount_percentage: Optional[Decimal]
    discount_amount: Optional[Decimal]
    coupon_code: Optional[str]
    referral_sales_partner: Optional[str]

    grand_total: Optional[Decimal]
    in_words: Optional[str]
    rounded_total: Optional[Decimal]
    rounding_adjustment: Optional[Decimal]
    disable_rounded_total: bool
    base_grand_total: Optional[Decimal]
    base_rounded_total: Optional[Decimal]

    payment_terms_template: Optional[str]
    payment_due_date: Optional[date]
    payment_amount: Optional[Decimal]

    tc_name: Optional[str]
    terms: Optional[str]

    letter_head: Optional[str]
    group_same_items: bool
    select_print_heading: Optional[str]
    language: Optional[str]

    auto_repeat_id: Optional[uuid.UUID]

    status: QuotationStatus

    rejection_reason: Optional[str]
    lost_reasons: Optional[list[str]]
    competitors: Optional[list[str]]

    customer_address: Optional[str]
    shipping_address: Optional[str]
    company_address: Optional[str]
    contact_person: Optional[str]
    contact_mobile: Optional[str]
    contact_email: Optional[str]

    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    utm_content: Optional[str]

    scan_barcode: Optional[str]
    supplier_quotation_id: Optional[uuid.UUID]
    customer_group: Optional[str]
    territory: Optional[str]

    items: list[QuotationItemResponse]
    taxes: list[QuotationTaxResponse]
    payment_schedule_entries: list[QuotationPaymentScheduleEntryResponse]

    created_at: datetime
    updated_at: Optional[datetime]


class QuotationListResponse(BaseModel):
    items: list[QuotationListItem]
    total: int
    page: int
    page_size: int