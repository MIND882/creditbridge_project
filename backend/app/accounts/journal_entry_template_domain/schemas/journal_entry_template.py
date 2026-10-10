"""Pydantic v2 schemas for JournalEntryTemplate."""



from __future__ import annotations



import uuid

from typing import Optional



from app.accounts.journal_entry_domain.models.journal_entry import JournalVoucherType, YesNo

from app.accounts.journal_entry_template_account_domain.schemas.journal_entry_template_account import (

    JournalEntryTemplateAccountCreate,

    JournalEntryTemplateAccountRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JournalEntryTemplateCreate",

    "JournalEntryTemplateUpdate",

    "JournalEntryTemplateRead",

    "JournalEntryTemplateListResponse",

]





class JournalEntryTemplateBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    voucher_type: JournalVoucherType

    naming_series: Optional[str] = None

    is_opening: Optional[YesNo] = YesNo.NO

    multi_currency: Optional[bool] = False





class JournalEntryTemplateCreate(JournalEntryTemplateBase):

    #: ``autoname = field:template_title``, so this is also the ``name``.

    template_title: str

    accounts: list[JournalEntryTemplateAccountCreate] = []





class JournalEntryTemplateUpdate(InputSchema):

    """

    A partial update.



    ``template_title`` is not patchable: upstream it *is* the ``name``, and

    renaming it would break every stored reference to the template.



    ``voucher_type`` is excluded for the same reason it is on ``TaxRuleUpdate``

    -- it decides how the template is meant to be used, and switching it in

    place would leave the account rows attached to a voucher type they were not

    chosen for. Omitted rather than declared-and-ignored, so ``extra="forbid"``

    rejects an attempt to send it.

    """



    naming_series: Optional[str] = None

    is_opening: Optional[YesNo] = None

    multi_currency: Optional[bool] = None

    accounts: Optional[list[JournalEntryTemplateAccountCreate]] = None





class JournalEntryTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    template_title: str

    voucher_type: JournalVoucherType

    naming_series: Optional[str] = None

    is_opening: YesNo

    multi_currency: bool

    accounts: list[JournalEntryTemplateAccountRead] = []





JournalEntryTemplateListResponse = Page[JournalEntryTemplateRead]
