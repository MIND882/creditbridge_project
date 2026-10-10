"""

Sales Invoice Timesheet -- converted from ``erpnext/accounts/doctype/sales_invoice_timesheet``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import DateTime, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesInvoiceTimesheet"]







class SalesInvoiceTimesheet(ChildTableModel, TenantModel):

    __tablename__ = "sales_invoice_timesheets"

    #: Polymorphic parent -- pos_invoice, sales_invoice

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    time_sheet: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    billing_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    timesheet_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    activity_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    to_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    project_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesInvoiceTimesheet id={self.id}>"
