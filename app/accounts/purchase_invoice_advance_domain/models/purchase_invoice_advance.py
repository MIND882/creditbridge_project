"""

Purchase Invoice Advance -- converted from ``erpnext/accounts/doctype/purchase_invoice_advance``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PurchaseInvoiceAdvance"]







class PurchaseInvoiceAdvance(ChildTableModel, TenantModel):

    __tablename__ = "purchase_invoice_advances"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_invoices.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PurchaseInvoice", back_populates="advances", foreign_keys=[parent_id])



    reference_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reference_row: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    advance_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    allocated_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    exchange_gain_loss: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ref_exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    difference_posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseInvoiceAdvance id={self.id}>"
