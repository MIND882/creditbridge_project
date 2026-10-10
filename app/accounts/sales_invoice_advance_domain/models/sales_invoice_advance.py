"""

Sales Invoice Advance -- converted from ``erpnext/accounts/doctype/sales_invoice_advance``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Numeric, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesInvoiceAdvance"]







class SalesInvoiceAdvance(ChildTableModel, TenantModel):

    __tablename__ = "sales_invoice_advances"

    #: Polymorphic parent -- pos_invoice, sales_invoice

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



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

        return f"<SalesInvoiceAdvance id={self.id}>"
