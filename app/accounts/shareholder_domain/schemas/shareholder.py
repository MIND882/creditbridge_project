"""Pydantic v2 schemas for Shareholder."""



from __future__ import annotations



import uuid

from typing import Optional



from app.accounts.share_balance_domain.schemas.share_balance import (

    ShareBalanceCreate,

    ShareBalanceRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShareholderCreate",

    "ShareholderUpdate",

    "ShareholderRead",

    "ShareholderListResponse",

]





class ShareholderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    title: str

    folio_no: Optional[str] = None

    #: A shareholder that is itself a company rather than a person.

    is_company: Optional[bool] = False

    #: Upstream a ``Code`` field holding serialised JSON from the desk UI.

    contact_list: Optional[str] = None





class ShareholderCreate(ShareholderBase):

    share_balance: list[ShareBalanceCreate] = []





class ShareholderUpdate(InputSchema):

    """

    A partial update.



    ``title`` is not the ``name`` here (``name`` comes from the naming series),

    so it is patchable -- upstream renames the shareholder's label freely.



    ``naming_series`` is not patchable: it decides the ``name``, and changing it

    after the fact would orphan every reference to this shareholder.

    """



    title: Optional[str] = None

    folio_no: Optional[str] = None

    is_company: Optional[bool] = None

    contact_list: Optional[str] = None

    share_balance: Optional[list[ShareBalanceCreate]] = None





class ShareholderRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: str

    title: str

    folio_no: Optional[str] = None

    is_company: bool

    contact_list: Optional[str] = None

    share_balance: list[ShareBalanceRead] = []





ShareholderListResponse = Page[ShareholderRead]
