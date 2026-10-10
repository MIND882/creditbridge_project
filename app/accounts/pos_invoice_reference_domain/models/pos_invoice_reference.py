"""

POS Invoice Reference -- converted from ``erpnext/accounts/doctype/pos_invoice_reference``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSInvoiceReference"]







class POSInvoiceReference(ChildTableModel, TenantModel):

    __tablename__ = "pos_invoice_references"

    #: Polymorphic parent -- pos_closing_entry, pos_invoice_merge_log

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    pos_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    grand_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    return_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSInvoiceReference id={self.id}>"
