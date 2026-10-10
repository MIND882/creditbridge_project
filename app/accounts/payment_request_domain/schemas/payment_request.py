"""Pydantic v2 schemas for PaymentRequest."""





from __future__ import annotations

from app.accounts.payment_request_domain.models.payment_request import (

    PaymentRequestNamingSeries,

    PaymentRequestPaymentChannel,

    PaymentRequestPaymentRequestType,

    PaymentRequestStatus,

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

from app.accounts.payment_reference_domain.schemas.payment_reference import (

    PaymentReferenceCreate,

    PaymentReferenceRead,

)



__all__ = [

    "PaymentRequestCreate",

    "PaymentRequestUpdate",

    "PaymentRequestRead",

    "PaymentRequestListResponse",

]





class PaymentRequestBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    payment_request_type: PaymentRequestPaymentRequestType = PaymentRequestPaymentRequestType.INWARD

    transaction_date: Optional[dt.date] = None

    naming_series: PaymentRequestNamingSeries = PaymentRequestNamingSeries.ACC_PRQ_YYYY

    mode_of_payment_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    grand_total: Optional[Decimal] = None

    is_a_subscription: bool = False

    currency: Optional[str] = None

    bank_account_id: Optional[uuid.UUID] = None

    bank_id: Optional[uuid.UUID] = None

    bank_account_no: Optional[str] = None

    account: Optional[str] = None

    iban: Optional[str] = None

    branch_code: Optional[str] = None

    swift_number: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    print_format: Optional[str] = None

    email_to: Optional[str] = None

    subject: Optional[str] = None

    payment_gateway_account: Optional[str] = None

    status: Optional[PaymentRequestStatus] = None

    make_sales_invoice: bool = False

    message: Optional[str] = None

    mute_email: bool = False

    payment_url: Optional[str] = None

    payment_gateway: Optional[str] = None

    payment_account: Optional[str] = None

    payment_channel: Optional[PaymentRequestPaymentChannel] = None

    payment_order: Optional[str] = None

    amended_from: Optional[str] = None

    failed_reason: Optional[str] = None

    outstanding_amount: Optional[Decimal] = None

    party_account_currency: Optional[str] = None

    party_name: Optional[str] = None

    phone_number: Optional[str] = None



    subscription_plans: list[SubscriptionPlanDetailCreate] = []



    payment_reference: list[PaymentReferenceCreate] = []





class PaymentRequestCreate(PaymentRequestBase):

    pass





class PaymentRequestUpdate(InputSchema):

    """A partial update."""



    payment_request_type: Optional[PaymentRequestPaymentRequestType] = None

    transaction_date: Optional[dt.date] = None

    naming_series: Optional[PaymentRequestNamingSeries] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    grand_total: Optional[Decimal] = None

    is_a_subscription: Optional[bool] = None

    currency: Optional[str] = None

    bank_account_id: Optional[uuid.UUID] = None

    bank_id: Optional[uuid.UUID] = None

    bank_account_no: Optional[str] = None

    account: Optional[str] = None

    iban: Optional[str] = None

    branch_code: Optional[str] = None

    swift_number: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    print_format: Optional[str] = None

    email_to: Optional[str] = None

    subject: Optional[str] = None

    payment_gateway_account: Optional[str] = None

    status: Optional[PaymentRequestStatus] = None

    make_sales_invoice: Optional[bool] = None

    message: Optional[str] = None

    mute_email: Optional[bool] = None

    payment_url: Optional[str] = None

    payment_gateway: Optional[str] = None

    payment_account: Optional[str] = None

    payment_channel: Optional[PaymentRequestPaymentChannel] = None

    payment_order: Optional[str] = None

    amended_from: Optional[str] = None

    failed_reason: Optional[str] = None

    outstanding_amount: Optional[Decimal] = None

    party_account_currency: Optional[str] = None

    party_name: Optional[str] = None

    phone_number: Optional[str] = None

    subscription_plans: Optional[list[SubscriptionPlanDetailCreate]] = None

    payment_reference: Optional[list[PaymentReferenceCreate]] = None





class PaymentRequestRead(ReadSchema):

    id: uuid.UUID

    name: str

    payment_request_type: PaymentRequestPaymentRequestType

    transaction_date: Optional[dt.date] = None

    naming_series: PaymentRequestNamingSeries

    mode_of_payment_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    grand_total: Decimal

    is_a_subscription: bool

    currency: Optional[str] = None

    bank_account_id: Optional[uuid.UUID] = None

    bank_id: Optional[uuid.UUID] = None

    bank_account_no: Optional[str] = None

    account: Optional[str] = None

    iban: Optional[str] = None

    branch_code: Optional[str] = None

    swift_number: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    print_format: Optional[str] = None

    email_to: Optional[str] = None

    subject: Optional[str] = None

    payment_gateway_account: Optional[str] = None

    status: Optional[PaymentRequestStatus] = None

    make_sales_invoice: bool

    message: Optional[str] = None

    mute_email: bool

    payment_url: Optional[str] = None

    payment_gateway: Optional[str] = None

    payment_account: Optional[str] = None

    payment_channel: Optional[PaymentRequestPaymentChannel] = None

    payment_order: Optional[str] = None

    amended_from: Optional[str] = None

    failed_reason: Optional[str] = None

    outstanding_amount: Optional[Decimal] = None

    party_account_currency: Optional[str] = None

    party_name: Optional[str] = None

    phone_number: Optional[str] = None

    subscription_plans: list[SubscriptionPlanDetailRead] = []

    payment_reference: list[PaymentReferenceRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





PaymentRequestListResponse = Page[PaymentRequestRead]
