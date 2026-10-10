"""

Discounted Invoice -- converted from ``erpnext/accounts/doctype/discounted_invoice``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["DiscountedInvoice"]







class DiscountedInvoice(ChildTableModel, TenantModel):

    __tablename__ = "discounted_invoices"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("invoice_discountings.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("InvoiceDiscounting", back_populates="invoices", foreign_keys=[parent_id])



    sales_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    debit_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    debit_to = relationship("Account", foreign_keys=[debit_to_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DiscountedInvoice id={self.id}>"
