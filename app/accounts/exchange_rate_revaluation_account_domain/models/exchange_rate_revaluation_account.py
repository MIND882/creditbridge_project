"""

Exchange Rate Revaluation Account -- converted from ``erpnext/accounts/doctype/exchange_rate_revaluation_account``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ExchangeRateRevaluationAccount"]







class ExchangeRateRevaluationAccount(ChildTableModel, TenantModel):

    __tablename__ = "exchange_rate_revaluation_accounts"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("exchange_rate_revaluations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ExchangeRateRevaluation", back_populates="accounts", foreign_keys=[parent_id])



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    balance_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    current_exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    balance_in_base_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    new_exchange_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    new_balance_in_base_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    gain_loss: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    zero_balance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    new_balance_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ExchangeRateRevaluationAccount id={self.id}>"
