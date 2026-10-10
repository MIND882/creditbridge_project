"""

Payment Reference -- converted from ``erpnext/accounts/doctype/payment_reference``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.payment_schedule_domain.models.payment_schedule import PaymentSchedule  # noqa: F401

from app.accounts.payment_term_domain.models.payment_term import PaymentTerm  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentReference"]







class PaymentReference(ChildTableModel, TenantModel):

    __tablename__ = "payment_references"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_requests.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PaymentRequest", back_populates="payment_reference", foreign_keys=[parent_id])



    payment_term_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_term = relationship("PaymentTerm", foreign_keys=[payment_term_id])

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    due_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_schedule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_schedules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_schedule = relationship("PaymentSchedule", foreign_keys=[payment_schedule_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentReference id={self.id}>"
