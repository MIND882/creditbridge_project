"""

PaymentEntryReference -- converted from ``erpnext/accounts/doctype/payment_entry_reference``.



Rows only ever exist inside a parent, so the API is read-only.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, Float, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentEntryReference"]





class PaymentEntryReference(ChildTableModel, TenantModel):

    """One row of ``PaymentEntry.references``."""



    __tablename__ = "payment_entry_references"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("payment_entries.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("PaymentEntry", back_populates="references", foreign_keys=[parent_id])



    reference_doctype: Mapped[str] = mapped_column(String(140), nullable=False)

    reference_name: Mapped[str] = mapped_column(String(140), nullable=False)

    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    bill_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    allocated_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    exchange_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    payment_term: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    exchange_gain_loss: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])

    account_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_request: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentEntryReference id={self.id}>"
