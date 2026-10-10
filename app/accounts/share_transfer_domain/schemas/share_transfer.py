"""Pydantic v2 schemas for ShareTransfer."""





from __future__ import annotations

from app.accounts.share_transfer_domain.models.share_transfer import (

    ShareTransferTransferType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShareTransferCreate",

    "ShareTransferUpdate",

    "ShareTransferRead",

    "ShareTransferListResponse",

]





class ShareTransferBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    transfer_type: ShareTransferTransferType

    date: dt.date

    from_shareholder_id: Optional[uuid.UUID] = None

    from_folio_no: Optional[str] = None

    equity_or_liability_account_id: uuid.UUID

    asset_account_id: Optional[uuid.UUID] = None

    to_shareholder_id: Optional[uuid.UUID] = None

    to_folio_no: Optional[str] = None

    share_type_id: uuid.UUID

    from_no: Optional[int] = None

    rate: Optional[Decimal] = None

    no_of_shares: Optional[int] = None

    to_no: Optional[int] = None

    amount: Optional[Decimal] = None

    remarks: Optional[str] = None

    amended_from: Optional[str] = None





class ShareTransferCreate(ShareTransferBase):

    pass





class ShareTransferUpdate(InputSchema):

    """A partial update."""



    transfer_type: Optional[ShareTransferTransferType] = None

    date: Optional[dt.date] = None

    from_shareholder_id: Optional[uuid.UUID] = None

    from_folio_no: Optional[str] = None

    equity_or_liability_account_id: Optional[uuid.UUID] = None

    asset_account_id: Optional[uuid.UUID] = None

    to_shareholder_id: Optional[uuid.UUID] = None

    to_folio_no: Optional[str] = None

    share_type_id: Optional[uuid.UUID] = None

    from_no: Optional[int] = None

    rate: Optional[Decimal] = None

    no_of_shares: Optional[int] = None

    to_no: Optional[int] = None

    amount: Optional[Decimal] = None

    remarks: Optional[str] = None

    amended_from: Optional[str] = None





class ShareTransferRead(ReadSchema):

    id: uuid.UUID

    name: str

    transfer_type: ShareTransferTransferType

    date: dt.date

    from_shareholder_id: Optional[uuid.UUID] = None

    from_folio_no: Optional[str] = None

    equity_or_liability_account_id: uuid.UUID

    asset_account_id: Optional[uuid.UUID] = None

    to_shareholder_id: Optional[uuid.UUID] = None

    to_folio_no: Optional[str] = None

    share_type_id: uuid.UUID

    from_no: int

    rate: Decimal

    no_of_shares: int

    to_no: int

    amount: Optional[Decimal] = None

    remarks: Optional[str] = None

    amended_from: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ShareTransferListResponse = Page[ShareTransferRead]
