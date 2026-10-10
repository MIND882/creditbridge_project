"""

Overdue Payment -- converted from ``erpnext/accounts/doctype/overdue_payment``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401

from app.accounts.payment_term_domain.models.payment_term import PaymentTerm  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["OverduePayment"]







class OverduePayment(ChildTableModel, TenantModel):

    __tablename__ = "overdue_payments"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("dunnings.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("Dunning", back_populates="overdue_payments", foreign_keys=[parent_id])



    payment_term_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_term = relationship("PaymentTerm", foreign_keys=[payment_term_id])

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    due_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    invoice_portion: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    payment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outstanding: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    paid_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discounted_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    sales_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    payment_schedule: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    overdue_days: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dunning_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<OverduePayment id={self.id}>"
