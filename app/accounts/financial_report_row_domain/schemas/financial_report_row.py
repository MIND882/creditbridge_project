"""Pydantic v2 schemas for FinancialReportRow."""





from __future__ import annotations

from app.accounts.financial_report_row_domain.models.financial_report_row import (

    FinancialReportRowBalanceType,

    FinancialReportRowDataSource,

    FinancialReportRowFieldtype,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "FinancialReportRowCreate",

    "FinancialReportRowRead",

    "FinancialReportRowListResponse",

]





class FinancialReportRowBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_code: Optional[str] = None

    display_name: Optional[str] = None

    indentation_level: Optional[int] = None

    data_source: Optional[FinancialReportRowDataSource] = None

    balance_type: Optional[FinancialReportRowBalanceType] = None

    bold_text: Optional[bool] = None

    italic_text: Optional[bool] = None

    hidden_calculation: Optional[bool] = None

    hide_when_empty: Optional[bool] = None

    reverse_sign: Optional[bool] = None

    calculation_formula: Optional[str] = None

    include_in_charts: Optional[bool] = None

    color: Optional[str] = None

    fieldtype: Optional[FinancialReportRowFieldtype] = None

    advanced_filtering: Optional[bool] = None





class FinancialReportRowCreate(FinancialReportRowBase):

    """Accepted only nested inside the parent payload."""

    pass





class FinancialReportRowRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    reference_code: Optional[str] = None

    display_name: Optional[str] = None

    indentation_level: Optional[int] = None

    data_source: Optional[FinancialReportRowDataSource] = None

    balance_type: Optional[FinancialReportRowBalanceType] = None

    bold_text: bool

    italic_text: bool

    hidden_calculation: bool

    hide_when_empty: bool

    reverse_sign: bool

    calculation_formula: Optional[str] = None

    include_in_charts: bool

    color: Optional[str] = None

    fieldtype: Optional[FinancialReportRowFieldtype] = None

    advanced_filtering: bool





FinancialReportRowListResponse = Page[FinancialReportRowRead]
