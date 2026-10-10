"""

Unreconcile Payment -- converted from ``erpnext/accounts/doctype/unreconcile_payment``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.unreconcile_payment_entries_domain.models.unreconcile_payment_entries import UnreconcilePaymentEntries



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["UnreconcilePayment"]







class UnreconcilePayment(SubmittableModel, TenantModel):

    __tablename__ = "unreconcile_payments"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_unreconcile_payments_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    allocations = relationship(

        UnreconcilePaymentEntries,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=UnreconcilePaymentEntries.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<UnreconcilePayment id={self.id}>"
