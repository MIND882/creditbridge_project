"""

Sales Invoice Reference -- converted from ``erpnext/accounts/doctype/sales_invoice_reference``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesInvoiceReference"]







class SalesInvoiceReference(ChildTableModel, TenantModel):

    __tablename__ = "sales_invoice_references"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_closing_entries.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSClosingEntry", back_populates="sales_invoices", foreign_keys=[parent_id])



    sales_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    return_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    grand_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesInvoiceReference id={self.id}>"
