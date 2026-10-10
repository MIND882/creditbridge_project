"""

Payment Reconciliation Invoice -- converted from ``erpnext/accounts/doctype/payment_reconciliation_invoice``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentReconciliationInvoice", "PaymentReconciliationInvoiceInvoiceType"]







class PaymentReconciliationInvoiceInvoiceType(str, enum.Enum):

    SALES_INVOICE = "Sales Invoice"

    PURCHASE_INVOICE = "Purchase Invoice"

    JOURNAL_ENTRY = "Journal Entry"









class PaymentReconciliationInvoice(ChildTableModel, TenantModel):

    __tablename__ = "payment_reconciliation_invoices"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_reconciliations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PaymentReconciliation", back_populates="invoices", foreign_keys=[parent_id])



    invoice_type: Mapped[Optional[PaymentReconciliationInvoiceInvoiceType]] = mapped_column(

        SAEnum(PaymentReconciliationInvoiceInvoiceType, native_enum=False, length=16, validate_strings=True),

        nullable=True,

    )

    invoice_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    invoice_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentReconciliationInvoice id={self.id}>"
