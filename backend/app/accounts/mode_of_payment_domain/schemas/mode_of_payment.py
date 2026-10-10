"""Pydantic v2 schemas for ModeOfPayment."""



from __future__ import annotations



import uuid

from typing import Optional



from app.accounts.mode_of_payment_account_domain.schemas.mode_of_payment_account import (

    ModeOfPaymentAccountCreate,

    ModeOfPaymentAccountRead,

)

from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPaymentType

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ModeOfPaymentCreate",

    "ModeOfPaymentUpdate",

    "ModeOfPaymentRead",

    "ModeOfPaymentListResponse",

]





class ModeOfPaymentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    type: Optional[ModeOfPaymentType] = None

    enabled: Optional[bool] = True





class ModeOfPaymentCreate(ModeOfPaymentBase):

    #: ``autoname = field:mode_of_payment``, so this is also the ``name``.

    mode_of_payment: str

    accounts: list[ModeOfPaymentAccountCreate] = []





class ModeOfPaymentUpdate(ModeOfPaymentBase):

    """

    A partial update.



    ``mode_of_payment`` is not patchable: upstream it *is* the ``name``, and

    renaming it would break every stored reference to this mode.

    """



    accounts: Optional[list[ModeOfPaymentAccountCreate]] = None





class ModeOfPaymentRead(ReadSchema):

    id: uuid.UUID

    name: str

    mode_of_payment: str

    type: Optional[ModeOfPaymentType] = None

    enabled: bool

    accounts: list[ModeOfPaymentAccountRead] = []





ModeOfPaymentListResponse = Page[ModeOfPaymentRead]
