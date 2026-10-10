"""

Bank Account Balance -- converted from ``erpnext/accounts/doctype/bank_account_balance``.



A Frappe child table (``istable: 1``): no independent identity, owned by a

Bank Account, ordered by ``idx``, never addressed by its own write API.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, ForeignKey, Numeric, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BankAccountBalance"]





class BankAccountBalance(ChildTableModel, TenantModel):

    """One row of a Bank Account."""



    __tablename__ = "bank_account_balances"



    #: Re-declared from the mixin with a concrete FK so the constraint is real.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", back_populates="balances")



    date: Mapped[date] = mapped_column(Date, nullable=False)

    balance: Mapped[Decimal] = mapped_column(Numeric(21,9), nullable=False)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankAccountBalance id={self.id}>"
