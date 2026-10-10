"""

Account Closing Balance -- converted from ``erpnext/accounts/doctype/account_closing_balance``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.finance_book_domain.models.finance_book import FinanceBook  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["AccountClosingBalance"]







class AccountClosingBalance(SubmittableModel, TenantModel):

    __tablename__ = "account_closing_balances"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_account_closing_balances_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    closing_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    debit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    credit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    debit_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    credit_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    finance_book_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("finance_books.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    finance_book = relationship("FinanceBook", foreign_keys=[finance_book_id])

    period_closing_voucher: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_period_closing_voucher_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    debit_in_reporting_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    credit_in_reporting_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reporting_currency_exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountClosingBalance id={self.id}>"
