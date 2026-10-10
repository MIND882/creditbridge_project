"""

BankTransactionRuleDescriptionCondition -- child table of BankTransactionRule, converted from

``erpnext/accounts/doctype/bank_transaction_rule_description_conditions``.



A child table (``istable: 1``): rows only ever exist inside a parent, so the API

is read-only by design -- writes happen through the parent's payload.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BankTransactionRuleDescriptionCondition"]





class BankTransactionRuleDescriptionCondition(ChildTableModel, TenantModel):

    """One row of ``BankTransactionRule.description_rules``."""



    __tablename__ = "bank_transaction_rule_description_conditions"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("bank_transaction_rules.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("BankTransactionRule", back_populates="description_rules", foreign_keys=[parent_id])



    check: Mapped[str] = mapped_column(String(20), nullable=False)

    value: Mapped[str] = mapped_column(Text, nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankTransactionRuleDescriptionCondition id={self.id} idx={self.idx}>"
