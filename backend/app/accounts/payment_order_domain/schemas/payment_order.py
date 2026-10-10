"""Pydantic v2 schemas for PaymentOrder."""





from __future__ import annotations

from app.accounts.payment_order_domain.models.payment_order import (

    PaymentOrderNamingSeries,

    PaymentOrderPaymentOrderType,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.payment_order_reference_domain.schemas.payment_order_reference import (

    PaymentOrderReferenceCreate,

    PaymentOrderReferenceRead,

)



__all__ = [

    "PaymentOrderCreate",

    "PaymentOrderUpdate",

    "PaymentOrderRead",

    "PaymentOrderListResponse",

]





class PaymentOrderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: PaymentOrderNamingSeries

    party: Optional[str] = None

    posting_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    payment_order_type: PaymentOrderPaymentOrderType

    company_bank_account_id: uuid.UUID

    company_bank_id: Optional[uuid.UUID] = None

    account: Optional[str] = None



    references: list[PaymentOrderReferenceCreate] = []





class PaymentOrderCreate(PaymentOrderBase):

    pass





class PaymentOrderUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[PaymentOrderNamingSeries] = None

    party: Optional[str] = None

    posting_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    payment_order_type: Optional[PaymentOrderPaymentOrderType] = None

    company_bank_account_id: Optional[uuid.UUID] = None

    company_bank_id: Optional[uuid.UUID] = None

    account: Optional[str] = None

    references: Optional[list[PaymentOrderReferenceCreate]] = None





class PaymentOrderRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: PaymentOrderNamingSeries

    party: Optional[str] = None

    posting_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    payment_order_type: PaymentOrderPaymentOrderType

    company_bank_account_id: uuid.UUID

    company_bank_id: Optional[uuid.UUID] = None

    account: Optional[str] = None

    references: list[PaymentOrderReferenceRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





PaymentOrderListResponse = Page[PaymentOrderRead]
