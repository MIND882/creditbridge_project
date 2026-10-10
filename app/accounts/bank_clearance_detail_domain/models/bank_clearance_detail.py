"""

BankClearanceDetail -- child table of BankClearance, converted from

``erpnext/accounts/doctype/bank_clearance_detail``.



A child table (``istable: 1``): rows only ever exist inside a parent, so the API

is read-only by design -- writes happen through the parent's payload.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BankClearanceDetail"]





class BankClearanceDetail(ChildTableModel, TenantModel):

    """One row of ``BankClearance.payment_entries``."""



    __tablename__ = "bank_clearance_details"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("bank_clearances.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("BankClearance", back_populates="payment_entries", foreign_keys=[parent_id])



    payment_document: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_entry: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    cheque_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cheque_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    clearance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankClearanceDetail id={self.id} idx={self.idx}>"
