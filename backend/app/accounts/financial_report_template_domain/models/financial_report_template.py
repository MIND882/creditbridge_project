"""

Financial Report Template -- converted from ``erpnext/accounts/doctype/financial_report_template``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.financial_report_row_domain.models.financial_report_row import FinancialReportRow



from app.core.base_model import TenantModel



__all__ = ["FinancialReportTemplate", "FinancialReportTemplateReportType"]







class FinancialReportTemplateReportType(str, enum.Enum):

    PROFIT_AND_LOSS_STATEMENT = "Profit and Loss Statement"

    BALANCE_SHEET = "Balance Sheet"

    CASH_FLOW = "Cash Flow"

    CUSTOM_FINANCIAL_STATEMENT = "Custom Financial Statement"









class FinancialReportTemplate(TenantModel):

    __tablename__ = "financial_report_templates"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_financial_report_templates_business_name"),

    )



    #: ``autoname`` = 'field:template_name'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    template_name: Mapped[str] = mapped_column(String(140), nullable=False)

    report_type: Mapped[FinancialReportTemplateReportType] = mapped_column(

        SAEnum(FinancialReportTemplateReportType, native_enum=False, length=26, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    module: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    rows = relationship(

        FinancialReportRow,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=FinancialReportRow.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<FinancialReportTemplate id={self.id}>"
