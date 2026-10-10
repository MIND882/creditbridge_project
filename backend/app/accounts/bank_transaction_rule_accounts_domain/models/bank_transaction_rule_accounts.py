"""

BankTransactionRuleAccount -- child table of BankTransactionRule, converted from

``erpnext/accounts/doctype/bank_transaction_rule_accounts``.



A child table (``istable: 1``): rows only ever exist inside a parent, so the API

is read-only by design -- writes happen through the parent's payload.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import ForeignKey, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BankTransactionRuleAccount"]





class BankTransactionRuleAccount(ChildTableModel, TenantModel):

    """One row of ``BankTransactionRule.accounts``."""



    __tablename__ = "bank_transaction_rule_accounts"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("bank_transaction_rules.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("BankTransactionRule", back_populates="accounts", foreign_keys=[parent_id])



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    debit: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    credit: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    user_remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankTransactionRuleAccount id={self.id} idx={self.idx}>"
