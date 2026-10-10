"""Pydantic v2 schemas for PaymentGatewayAccount."""





from __future__ import annotations

from app.accounts.payment_gateway_account_domain.models.payment_gateway_account import (

    PaymentGatewayAccountPaymentChannel,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentGatewayAccountCreate",

    "PaymentGatewayAccountUpdate",

    "PaymentGatewayAccountRead",

    "PaymentGatewayAccountListResponse",

]





class PaymentGatewayAccountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    payment_gateway: str

    is_default: Optional[bool] = None

    payment_account_id: uuid.UUID

    currency: Optional[str] = None

    message: Optional[str] = None

    payment_channel: Optional[PaymentGatewayAccountPaymentChannel] = None





class PaymentGatewayAccountCreate(PaymentGatewayAccountBase):

    pass





class PaymentGatewayAccountUpdate(InputSchema):

    """A partial update."""



    payment_gateway: Optional[str] = None

    is_default: Optional[bool] = None

    payment_account_id: Optional[uuid.UUID] = None

    currency: Optional[str] = None

    message: Optional[str] = None

    payment_channel: Optional[PaymentGatewayAccountPaymentChannel] = None





class PaymentGatewayAccountRead(ReadSchema):

    id: uuid.UUID

    name: str

    payment_gateway: str

    is_default: bool

    payment_account_id: uuid.UUID

    currency: Optional[str] = None

    message: Optional[str] = None

    payment_channel: Optional[PaymentGatewayAccountPaymentChannel] = None





PaymentGatewayAccountListResponse = Page[PaymentGatewayAccountRead]
