"""

Bank Reconciliation Tool -- converted from ``erpnext/accounts/doctype/bank_reconciliation_tool``.





"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.bank_account_domain.models.bank_account import BankAccount  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["BankReconciliationTool"]







class BankReconciliationTool(TenantModel):

    __tablename__ = "bank_reconciliation_tools"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bank_reconciliation_tools_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    bank_statement_from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    bank_statement_to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    account_opening_balance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    bank_statement_closing_balance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    from_reference_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_reference_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    filter_by_reference_date: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankReconciliationTool id={self.id}>"
