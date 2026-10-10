"""

Financial Report Row -- converted from ``erpnext/accounts/doctype/financial_report_row``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Integer, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["FinancialReportRow", "FinancialReportRowDataSource", "FinancialReportRowBalanceType", "FinancialReportRowFieldtype"]







class FinancialReportRowDataSource(str, enum.Enum):

    ACCOUNT_DATA = "Account Data"

    CALCULATED_AMOUNT = "Calculated Amount"

    CUSTOM_API = "Custom API"

    BLANK_LINE = "Blank Line"

    COLUMN_BREAK = "Column Break"

    SECTION_BREAK = "Section Break"





class FinancialReportRowBalanceType(str, enum.Enum):

    OPENING_BALANCE = "Opening Balance"

    CLOSING_BALANCE = "Closing Balance"

    PERIOD_MOVEMENT_DEBITS_CREDITS = "Period Movement (Debits - Credits)"





class FinancialReportRowFieldtype(str, enum.Enum):

    CURRENCY = "Currency"

    FLOAT = "Float"

    INT = "Int"

    PERCENT = "Percent"









class FinancialReportRow(ChildTableModel, TenantModel):

    __tablename__ = "financial_report_rows"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("financial_report_templates.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("FinancialReportTemplate", back_populates="rows", foreign_keys=[parent_id])



    reference_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    display_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    indentation_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    data_source: Mapped[Optional[FinancialReportRowDataSource]] = mapped_column(

        SAEnum(FinancialReportRowDataSource, native_enum=False, length=17, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    balance_type: Mapped[Optional[FinancialReportRowBalanceType]] = mapped_column(

        SAEnum(FinancialReportRowBalanceType, native_enum=False, length=34, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    bold_text: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    italic_text: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    hidden_calculation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    hide_when_empty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    reverse_sign: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    calculation_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    include_in_charts: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    color: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fieldtype: Mapped[Optional[FinancialReportRowFieldtype]] = mapped_column(

        SAEnum(FinancialReportRowFieldtype, native_enum=False, length=8, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    advanced_filtering: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<FinancialReportRow id={self.id}>"
