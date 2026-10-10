"""Pydantic v2 schemas for FinancialReportTemplate."""





from __future__ import annotations

from app.accounts.financial_report_template_domain.models.financial_report_template import (

    FinancialReportTemplateReportType,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.financial_report_row_domain.schemas.financial_report_row import (

    FinancialReportRowCreate,

    FinancialReportRowRead,

)



__all__ = [

    "FinancialReportTemplateCreate",

    "FinancialReportTemplateUpdate",

    "FinancialReportTemplateRead",

    "FinancialReportTemplateListResponse",

]





class FinancialReportTemplateBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    template_name: str

    report_type: FinancialReportTemplateReportType

    module: Optional[str] = None

    disabled: Optional[bool] = None



    rows: list[FinancialReportRowCreate] = []





class FinancialReportTemplateCreate(FinancialReportTemplateBase):

    pass





class FinancialReportTemplateUpdate(InputSchema):

    """A partial update."""



    template_name: Optional[str] = None

    report_type: Optional[FinancialReportTemplateReportType] = None

    module: Optional[str] = None

    disabled: Optional[bool] = None

    rows: Optional[list[FinancialReportRowCreate]] = None





class FinancialReportTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    template_name: str

    report_type: FinancialReportTemplateReportType

    module: Optional[str] = None

    disabled: bool

    rows: list[FinancialReportRowRead] = []





FinancialReportTemplateListResponse = Page[FinancialReportTemplateRead]
