"""

POS Payment Method -- converted from ``erpnext/accounts/doctype/pos_payment_method``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSPaymentMethod"]







class POSPaymentMethod(ChildTableModel, TenantModel):

    __tablename__ = "pos_payment_methods"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_profiles.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSProfile", back_populates="payments", foreign_keys=[parent_id])



    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    allow_in_returns: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSPaymentMethod id={self.id}>"
