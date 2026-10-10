"""

BankTransactionPayment -- child table of BankTransaction, converted from

``erpnext/accounts/doctype/bank_transaction_payments``.



A child table (``istable: 1``): rows only ever exist inside a parent, so the API

is read-only by design -- writes happen through the parent's payload.

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



__all__ = ["BankTransactionPayment"]





class BankTransactionPayment(ChildTableModel, TenantModel):

    """One row of ``BankTransaction.payment_entries``."""



    __tablename__ = "bank_transaction_payments"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("acc_bank_transactions.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("app.accounts.bank_transaction_domain.models.bank_transaction.BankTransaction", back_populates="payment_entries", foreign_keys=[parent_id])



    payment_document: Mapped[str] = mapped_column(String(140), nullable=False)

    payment_entry: Mapped[str] = mapped_column(String(140), nullable=False)

    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)

    clearance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    reconciliation_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankTransactionPayment id={self.id} idx={self.idx}>"
