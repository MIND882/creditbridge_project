"""

Sales Invoice Payment -- converted from ``erpnext/accounts/doctype/sales_invoice_payment``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesInvoicePayment"]







class SalesInvoicePayment(ChildTableModel, TenantModel):

    __tablename__ = "sales_invoice_payments"

    #: Polymorphic parent -- pos_invoice, sales_invoice

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    clearance_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    reference_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesInvoicePayment id={self.id}>"
