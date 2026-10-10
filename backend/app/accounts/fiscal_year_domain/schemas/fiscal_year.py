"""Pydantic v2 schemas for FiscalYear."""



from __future__ import annotations



import datetime as dt

import uuid

from typing import Optional



from app.accounts.fiscal_year_company_domain.schemas.fiscal_year_company import (

    FiscalYearCompanyCreate,

    FiscalYearCompanyRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "FiscalYearCreate",

    "FiscalYearUpdate",

    "FiscalYearRead",

    "FiscalYearListResponse",

]





class FiscalYearBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    #: ``autoname = field:year``, so this is also the ``name``.

    year: str

    year_start_date: dt.date

    year_end_date: dt.date

    disabled: Optional[bool] = False

    #: Exempts this year from the "exactly one year" rule.

    is_short_year: Optional[bool] = False





class FiscalYearCreate(FiscalYearBase):

    companies: list[FiscalYearCompanyCreate] = []





class FiscalYearUpdate(InputSchema):

    """

    A partial update.



    ``year`` is not patchable: upstream it *is* the ``name``, and renaming it

    would break every voucher that records which fiscal year it posted into.



    ``auto_created`` is also absent -- it records provenance (the scheduler

    rolled this year forward), which is not something a client gets to assert.

    """



    year_start_date: Optional[dt.date] = None

    year_end_date: Optional[dt.date] = None

    disabled: Optional[bool] = None

    is_short_year: Optional[bool] = None

    companies: Optional[list[FiscalYearCompanyCreate]] = None





class FiscalYearRead(ReadSchema):

    id: uuid.UUID

    name: str

    year: str

    year_start_date: dt.date

    year_end_date: dt.date

    disabled: bool

    auto_created: bool

    is_short_year: bool

    companies: list[FiscalYearCompanyRead] = []





FiscalYearListResponse = Page[FiscalYearRead]
