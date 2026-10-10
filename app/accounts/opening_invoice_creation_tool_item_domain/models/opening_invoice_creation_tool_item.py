"""

Opening Invoice Creation Tool Item -- converted from ``erpnext/accounts/doctype/opening_invoice_creation_tool_item``.



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

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["OpeningInvoiceCreationToolItem"]







class OpeningInvoiceCreationToolItem(ChildTableModel, TenantModel):

    __tablename__ = "opening_invoice_creation_tool_items"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("opening_invoice_creation_tools.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("OpeningInvoiceCreationTool", back_populates="invoices", foreign_keys=[parent_id])



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    temporary_opening_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    temporary_opening_account = relationship("Account", foreign_keys=[temporary_opening_account_id])

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    due_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    outstanding_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    qty: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    invoice_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_invoice_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    party_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<OpeningInvoiceCreationToolItem id={self.id}>"
