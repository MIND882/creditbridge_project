"""Pydantic v2 schemas for Subscription."""





from __future__ import annotations

from app.accounts.subscription_domain.models.subscription import (

    SubscriptionApplyAdditionalDiscount,

    SubscriptionGenerateInvoiceAt,

    SubscriptionStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.subscription_plan_detail_domain.schemas.subscription_plan_detail import (

    SubscriptionPlanDetailCreate,

    SubscriptionPlanDetailRead,

)



__all__ = [

    "SubscriptionCreate",

    "SubscriptionUpdate",

    "SubscriptionRead",

    "SubscriptionListResponse",

]





class SubscriptionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    status: Optional[SubscriptionStatus] = None

    cancelation_date: Optional[dt.date] = None

    trial_period_start: Optional[dt.date] = None

    trial_period_end: Optional[dt.date] = None

    current_invoice_start: Optional[dt.date] = None

    current_invoice_end: Optional[dt.date] = None

    next_billing_period_start: Optional[dt.date] = None

    next_billing_period_end: Optional[dt.date] = None

    days_until_due: Optional[int] = None

    cancel_at_period_end: Optional[bool] = None

    apply_additional_discount: Optional[SubscriptionApplyAdditionalDiscount] = None

    additional_discount_percentage: Optional[Decimal] = None

    additional_discount_amount: Optional[Decimal] = None

    party_type: str

    party: Optional[str] = None

    sales_tax_template: Optional[str] = None

    purchase_tax_template: Optional[str] = None

    follow_calendar_months: Optional[bool] = None

    generate_new_invoices_past_due_date: Optional[bool] = None

    end_date: Optional[dt.date] = None

    start_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    submit_invoice: Optional[bool] = None

    generate_invoice_at: SubscriptionGenerateInvoiceAt

    number_of_days: Optional[int] = None



    plans: list[SubscriptionPlanDetailCreate] = []





class SubscriptionCreate(SubscriptionBase):

    pass





class SubscriptionUpdate(InputSchema):

    """A partial update."""



    status: Optional[SubscriptionStatus] = None

    cancelation_date: Optional[dt.date] = None

    trial_period_start: Optional[dt.date] = None

    trial_period_end: Optional[dt.date] = None

    current_invoice_start: Optional[dt.date] = None

    current_invoice_end: Optional[dt.date] = None

    next_billing_period_start: Optional[dt.date] = None

    next_billing_period_end: Optional[dt.date] = None

    days_until_due: Optional[int] = None

    cancel_at_period_end: Optional[bool] = None

    apply_additional_discount: Optional[SubscriptionApplyAdditionalDiscount] = None

    additional_discount_percentage: Optional[Decimal] = None

    additional_discount_amount: Optional[Decimal] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    sales_tax_template: Optional[str] = None

    purchase_tax_template: Optional[str] = None

    follow_calendar_months: Optional[bool] = None

    generate_new_invoices_past_due_date: Optional[bool] = None

    end_date: Optional[dt.date] = None

    start_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    submit_invoice: Optional[bool] = None

    generate_invoice_at: Optional[SubscriptionGenerateInvoiceAt] = None

    number_of_days: Optional[int] = None

    plans: Optional[list[SubscriptionPlanDetailCreate]] = None





class SubscriptionRead(ReadSchema):

    id: uuid.UUID

    name: str

    status: Optional[SubscriptionStatus] = None

    cancelation_date: Optional[dt.date] = None

    trial_period_start: Optional[dt.date] = None

    trial_period_end: Optional[dt.date] = None

    current_invoice_start: Optional[dt.date] = None

    current_invoice_end: Optional[dt.date] = None

    next_billing_period_start: Optional[dt.date] = None

    next_billing_period_end: Optional[dt.date] = None

    days_until_due: Optional[int] = None

    cancel_at_period_end: bool

    apply_additional_discount: Optional[SubscriptionApplyAdditionalDiscount] = None

    additional_discount_percentage: Optional[Decimal] = None

    additional_discount_amount: Optional[Decimal] = None

    party_type: str

    party: Optional[str] = None

    sales_tax_template: Optional[str] = None

    purchase_tax_template: Optional[str] = None

    follow_calendar_months: bool

    generate_new_invoices_past_due_date: bool

    end_date: Optional[dt.date] = None

    start_date: Optional[dt.date] = None

    cost_center_id: Optional[uuid.UUID] = None

    submit_invoice: bool

    generate_invoice_at: SubscriptionGenerateInvoiceAt

    number_of_days: Optional[int] = None

    plans: list[SubscriptionPlanDetailRead] = []





SubscriptionListResponse = Page[SubscriptionRead]
