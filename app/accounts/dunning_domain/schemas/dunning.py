"""Pydantic v2 schemas for Dunning."""





from __future__ import annotations

from app.accounts.dunning_domain.models.dunning import (

    DunningNamingSeries,

    DunningStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.overdue_payment_domain.schemas.overdue_payment import (

    OverduePaymentCreate,

    OverduePaymentRead,

)



__all__ = [

    "DunningCreate",

    "DunningUpdate",

    "DunningRead",

    "DunningListResponse",

]





class DunningBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[DunningNamingSeries] = None

    customer_name: Optional[str] = None

    posting_date: dt.date

    dunning_type_id: Optional[uuid.UUID] = None

    dunning_fee: Optional[Decimal] = None

    language: Optional[str] = None

    letter_head: Optional[str] = None

    amended_from: Optional[str] = None

    body_text: Optional[str] = None

    closing_text: Optional[str] = None

    posting_time: Optional[dt.time] = None

    rate_of_interest: Optional[Decimal] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    company_address_display: Optional[str] = None

    contact_email: Optional[str] = None

    customer: str

    grand_total: Optional[Decimal] = None

    status: Optional[DunningStatus] = None

    income_account_id: Optional[uuid.UUID] = None

    total_interest: Optional[Decimal] = None

    total_outstanding: Optional[Decimal] = None

    customer_address: Optional[str] = None

    contact_person: Optional[str] = None

    dunning_amount: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    spacer: Optional[str] = None

    company_address: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    base_dunning_amount: Optional[Decimal] = None



    overdue_payments: list[OverduePaymentCreate] = []





class DunningCreate(DunningBase):

    pass





class DunningUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[DunningNamingSeries] = None

    customer_name: Optional[str] = None

    posting_date: Optional[dt.date] = None

    dunning_type_id: Optional[uuid.UUID] = None

    dunning_fee: Optional[Decimal] = None

    language: Optional[str] = None

    letter_head: Optional[str] = None

    amended_from: Optional[str] = None

    body_text: Optional[str] = None

    closing_text: Optional[str] = None

    posting_time: Optional[dt.time] = None

    rate_of_interest: Optional[Decimal] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    company_address_display: Optional[str] = None

    contact_email: Optional[str] = None

    customer: Optional[str] = None

    grand_total: Optional[Decimal] = None

    status: Optional[DunningStatus] = None

    income_account_id: Optional[uuid.UUID] = None

    total_interest: Optional[Decimal] = None

    total_outstanding: Optional[Decimal] = None

    customer_address: Optional[str] = None

    contact_person: Optional[str] = None

    dunning_amount: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    spacer: Optional[str] = None

    company_address: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    base_dunning_amount: Optional[Decimal] = None

    overdue_payments: Optional[list[OverduePaymentCreate]] = None





class DunningRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[DunningNamingSeries] = None

    customer_name: Optional[str] = None

    posting_date: dt.date

    dunning_type_id: Optional[uuid.UUID] = None

    dunning_fee: Optional[Decimal] = None

    language: Optional[str] = None

    letter_head: Optional[str] = None

    amended_from: Optional[str] = None

    body_text: Optional[str] = None

    closing_text: Optional[str] = None

    posting_time: Optional[dt.time] = None

    rate_of_interest: Optional[Decimal] = None

    address_display: Optional[str] = None

    contact_display: Optional[str] = None

    contact_mobile: Optional[str] = None

    company_address_display: Optional[str] = None

    contact_email: Optional[str] = None

    customer: str

    grand_total: Optional[Decimal] = None

    status: Optional[DunningStatus] = None

    income_account_id: Optional[uuid.UUID] = None

    total_interest: Optional[Decimal] = None

    total_outstanding: Optional[Decimal] = None

    customer_address: Optional[str] = None

    contact_person: Optional[str] = None

    dunning_amount: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    spacer: Optional[str] = None

    company_address: Optional[str] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    base_dunning_amount: Optional[Decimal] = None

    overdue_payments: list[OverduePaymentRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





DunningListResponse = Page[DunningRead]
